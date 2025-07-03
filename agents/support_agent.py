import re
from datetime import datetime
# from googletrans import Translator

class SupportAgent:
    """
    SupportAgent

    This agent handles client-facing queries related to:
    1. Client Information
    2. Order Management
    3. Payment Info
    4. Course/Class Discovery
    5. External API usage for enquiry/order creation
    """

    def __init__(self, db_tool, api_tool):
        """
        Initialize SupportAgent with database and external API tools.
        """
        self.db_tool = db_tool
        self.api_tool = api_tool
        # self.translator = Translator()

    def translate_prompt(self, prompt: str) -> str:
        try:
            translated = self.translator.translate(prompt, dest='en')
            return translated.text.lower()
        except Exception:
            return prompt.lower() 

    def handle_client_query(self, prompt: str):
        """
        Main dispatcher to handle natural language client queries.
        Routes prompt to appropriate functionality based on keyword match.
        """
        #prompt = self.translate_prompt(prompt)
        #print(prompt)

        prompt = prompt.lower().strip()

        if "create an order" in prompt:
            return self.create_order_flow(prompt)
        elif "has order" in prompt:
            return self.check_order_status(prompt)
        elif "payment" in prompt and "due" in prompt:
            return self.calculate_payment_due(prompt)
        elif "available classes" in prompt or "this week" in prompt:
            return self.list_classes()
        elif "create enquiry" in prompt:
            return self.create_enquiry(prompt)
        elif "search client" in prompt:
            return self.search_client(prompt)
        elif "orders for client" in prompt:
            return self.get_orders_by_client(prompt)
        elif "orders with status" in prompt or "paid orders" in prompt or "pending orders" in prompt:
            return self.filter_orders_by_status(prompt)
        elif "filter classes" in prompt or "classes by instructor" in prompt:
            return self.filter_classes_by_instructor(prompt)
        else:
            return {"message": "Sorry, I didn't understand the request."}

    # ================================
    # 1. CLIENT DATA
    # ================================

    def search_client(self, prompt: str):
        """
        Search client by name, email, or phone number.
        """
        try:
            query = re.search(r"(name|email|phone)\s+(\S+)", prompt)
            if not query:
                return {"error": "Please specify name, email, or phone to search."}

            field, value = query.groups()
            client = self.db_tool.find_one("clients", {
                field: {"$regex": value, "$options": "i"}
            })

            if client:
                return {"client": client}
            else:
                return {"error": f"No client found with {field}: {value}"}
        except Exception as e:
            return {"error": f"An error occurred while searching for the client: {str(e)}"}

    def get_orders_by_client(self, prompt: str):
        """
        View all enrolled services (orders) for a client.
        """
        try:
            match = re.search(r'client\s+(.+)', prompt)
            if not match:
                return {"error": "Please provide a client name."}

            client_name = match.group(1).strip()
            client = self.db_tool.find_one("clients", {
                "name": {"$regex": client_name, "$options": "i"}
            })

            if not client:
                return {"error": f"No client found with name '{client_name}'"}

            orders = self.db_tool.find("orders", {"client_id": client["_id"]})
            return {"client_name": client_name, "orders": orders}

        except Exception as e: 
            return {"error": f"An error occurred while retrieving orders for the client: {str(e)}"}
    # ================================
    # 2. ORDER MANAGEMENT
    # ================================

    def create_order_flow(self, prompt: str):
        """
        Create a new order for a service on behalf of a client.
        """
        try:
            if "for" in prompt:
                parts = prompt.lower().replace("create an order", "").rsplit("for", 1)
                service = parts[0].strip()
                client_name = parts[1].strip()

                client = self.db_tool.find_one("clients", {
                    "name": {
                        "$regex": client_name,
                        "$options": "i"
                    }
                })
                if not client:
                    return {"error": f"No client found with name '{client_name}'"}

                order = self.api_tool.create_order(client_id=client["_id"], service_name=service)
                self.db_tool.insert("orders", order)
                return {
                    "message": f"Order created successfully for {client_name} with service {service}.",
                    "order_id": order["order_id"]
                }
            return {"error": "Invalid order creation request. Please specify the service and client name."}
        except Exception as e:
            return {"error": f"An error occurred while creating the order: {str(e)}"}

    def check_order_status(self, prompt: str):
        """
        Get the status of a specific order by order ID.
        """
        try:
            match = re.search(r'order #?(\w+)', prompt)
            if match:
                order_id = match.group(1)
                order = self.db_tool.find_one("orders", {"order_id": order_id})
                if order:
                    return {"message": f"Order {order_id} status: {order['status']}"}
                else:
                    return {"error": f"No order found with ID {order_id}"}
            return {"error": "Please specify the order ID to check its status."}
        except Exception as e:
            return {"error": f"An error occurred while checking the order status: {str(e)}"}

    def filter_orders_by_status(self, prompt: str):
        """
        Filter orders based on status: paid or pending.
        """
        try:
            if "pending" in prompt:
                status = "pending"
            elif "paid" in prompt:
                status = "paid"
            else:
                return {"error": "Please specify a valid status (paid or pending)."}

            orders = self.db_tool.find("orders", {"status": status})
            return {"status": status, "orders": orders}
        except Exception as e:
            return {"error": f"An error occurred while filtering orders by status: {str(e)}"}
    # ================================
    # 3. PAYMENT INFORMATION
    # ================================

    def calculate_payment_due(self, prompt: str):
        """
        Calculate pending dues for an order.
        """
        try:
            match = re.search(r'order #?(\w+)', prompt)
            if match:
                order_id = match.group(1)
                order = self.db_tool.find_one("orders", {"order_id": order_id})
                if not order:
                    return {"error": "Order not found"}

                payment = self.db_tool.find_one("payments", {"order_id": order_id})

                amount = order.get("amount", 0)
                paid = payment.get("paid", 0) if payment else 0

                due = max(amount - paid, 0)

                return {
                    "order_id": order_id,
                    "total_amount": amount,
                    "amount_paid": paid,
                    "due_amount": due
                }

            return {"error": "Please mention the order ID."}
        except Exception as e:
            return {"error": f"An error occurred while calculating payment due: {str(e)}"}

    # ================================
    # 4. COURSE / CLASS DISCOVERY
    # ================================

    def list_classes(self):
        """
        List all upcoming classes from today onwards.
        """
        try:
            today = datetime.today().isoformat()
            classes = self.db_tool.find("classes", {"start_time": {"$gte": today}})
            for cls in classes:
                if "_id" in cls:
                    cls["_id"] = str(cls["_id"])
                if "start_time" in cls:
                    cls["start_time"] = cls["start_time"].isoformat() if isinstance(cls["start_time"], datetime) else cls["start_time"]
            return {"upcoming_classes": classes}
        except Exception as e:
            return {"error": f"An error occurred while listing classes: {str(e)}"}

    def filter_classes_by_instructor(self, prompt: str):
        try:
            filters={}
            match = re.search(r"instructor\s+(\w+)", prompt)
            if match:
                filters["instructor"] = {"$regex": match.group(1), "$options": "i"}
            
            if "completed" in prompt:
                filters["status"] = "completed"
            elif "scheduled" in prompt:
                filters["status"] = "scheduled"
            
            records = self.db_tool.find("classes", filters)
            for record in records:
                if "_id" in record:
                    record["_id"] = str(record["_id"])

            return {"filtered_classes": records}
        except Exception as e:
            return {"error": f"An error occurred while filtering classes: {str(e)}"}

    # ================================
    # 5. EXTERNAL API USAGE
    # ================================

    def create_enquiry(self, prompt: str):
        """
        Create a new client enquiry via External API.
        """
        try:
            client_name = prompt.lower().replace("create enquiry for", "").strip()

            enquiry = self.api_tool.create_enquiry(client_name)
            self.db_tool.insert("enquiries", enquiry)

            return {"message": f"Enquiry created for {client_name}", "enquiry_id": enquiry["enquiry_id"]}
        except Exception as e:
            return {"error": f"An error occurred while creating the enquiry: {str(e)}"}