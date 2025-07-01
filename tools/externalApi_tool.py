import uuid
import datetime

class ExternalApiTool:
    def create_order(self,client_id: str, service_name: str):
        return {
            "order_id": str(uuid.uuid4()),
            "client_id": client_id,
            "service_name": service_name,
            "status": "pending",
            "created_at": datetime.datetime.now().isoformat(),
        }
    
    def create_client_enquiry(self, name: str, email: str, ohone: str):
        return {
            "enquiry_id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "phone": ohone,
            "status": "new",
            "created_at": datetime.datetime.now().isoformat(),
        }