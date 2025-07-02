from datetime import datetime, timedelta


class DashboardAgent:
    def __init__(self, db_tool):
        self.db = db_tool

    def handle_query(self, prompt: str):
        """
        Routes the incoming prompt to the appropriate analytics function.
        """
        prompt = prompt.lower()

        if "revenue" in prompt:
            return self.total_revenue()
        elif "outstanding payments" in prompt:
            return self.outstanding_payments()
        elif "inactive clients" in prompt:
            return self.inactive_clients()
        elif "birthday" in prompt:
            return self.birthday_reminders()
        elif "new clients" in prompt:
            return self.new_clients_this_month()
        elif "enrollment trends" in prompt:
            return self.enrollment_trends()
        elif "top service" in prompt or "highest enrollment" in prompt:
            return self.top_services()
        elif "completion rate" in prompt:
            return self.course_completion_rates()
        elif "attendance" in prompt and "percentage" in prompt:
            return self.attendance_by_class(prompt)
        elif "drop-off" in prompt:
            return self.drop_off_rates()
        else:
            return {"message": "Query not recognized for dashboard agent."}

    # ----------------------------------------
    # Revenue Metrics
    # ----------------------------------------

    def total_revenue(self):
        """
        Returns the total revenue by summing all 'paid' values in the 'payments' collection.
        """
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$paid"}}}
        ]
        result = self.db.aggregate("payments", pipeline)
        total = result[0]["total"] if result else 0
        return {"total_revenue": total}

    def outstanding_payments(self):
        """
        Calculates outstanding payments by comparing order amount vs paid amount.
        """
        orders = self.db.find("orders", {})
        payments = self.db.find("payments", {})

        paid_map = {p["order_id"]: p["paid"] for p in payments}
        dues = 0

        for order in orders:
            amount = order.get("amount", 0)
            paid = paid_map.get(order["order_id"], 0)
            if paid < amount:
                dues += (amount - paid)

        return {"outstanding_dues": dues}

    # ----------------------------------------
    # Client Insights
    # ----------------------------------------

    def inactive_clients(self):
        """
        Returns the number of clients whose status is marked as 'inactive'.
        """
        clients = self.db.find("clients", {"status": "inactive"})
        return {"inactive_clients": len(clients)}

    def birthday_reminders(self):
        """
        Returns clients who have birthdays today, matching on MM-DD format in 'dob'.
        """
        today = datetime.today()
        this_month = today.month
        this_day = today.day

        clients = self.db.find("clients", {
            "dob": {
                "$regex": f"-{this_month:02d}-{this_day:02d}$"
            }
        })
        return {"birthdays_today": [c["name"] for c in clients]}

    def new_clients_this_month(self):
        """
        Returns the count of clients created since the first of the current month.
        """
        first_day = datetime.today().replace(day=1)
        clients = self.db.find("clients", {
            "created_at": {"$gte": first_day.isoformat()}
        })
        return {"new_clients": len(clients)}

    # ----------------------------------------
    # Service Analytics
    # ----------------------------------------

    def enrollment_trends(self):
        """
        Aggregates and returns count of enrollments (orders) by service_name.
        """
        pipeline = [
            {"$group": {"_id": "$service_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        result = self.db.aggregate("orders", pipeline)
        return {"enrollment_trends": result}

    def top_services(self):
        """
        Returns the top 3 most enrolled services based on order count.
        """
        pipeline = [
            {"$group": {"_id": "$service_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 3}
        ]
        result = self.db.aggregate("orders", pipeline)
        return {"top_services": result}

    def course_completion_rates(self):
        """
        Returns a list of courses with their respective completion rates.
        """
        courses = self.db.find("courses", {})
        completions = [
            {"course": c["title"], "completion_rate": c.get("completion_rate", 0)}
            for c in courses
        ]
        return {"completion_rates": completions}

    # ----------------------------------------
    # Attendance Reports
    # ----------------------------------------

    def attendance_by_class(self, prompt):
        """
        Calculates attendance percentage for a given class using records in 'attendance'.
        """
        import re
        match = re.search(r'attendance percentage for ([\w\s]+)', prompt)
        class_name = match.group(1).strip() if match else None

        if not class_name:
            return {"error": "Class name not specified"}

        records = self.db.find("attendance", {"class": {"$regex": class_name, "$options": "i"}})
        total = len(records)
        present = sum(1 for r in records if r.get("present") is True)
        percent = round((present / total) * 100, 2) if total else 0

        return {"class": class_name, "attendance_percentage": percent}

    def drop_off_rates(self):
        """
        Counts how many clients have missed 2 or more sessions (drop-off risk).
        """
        records = self.db.find("attendance", {})
        dropout_map = {}
        for r in records:
            cid = r.get("client_id")
            if r.get("present") is False:
                dropout_map[cid] = dropout_map.get(cid, 0) + 1

        drop_count = sum(1 for c in dropout_map.values() if c >= 2)
        return {"drop_off_count": drop_count}
