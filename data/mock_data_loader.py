import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta ,UTC

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info() 
    db = client[MONGO_DB]
    print(f"Connected to MongoDB Cloud: {MONGO_DB}")
except Exception as e:
    print("Connection error:", e)
    exit()

# Drop old data
collections = ["clients", "orders", "payments", "classes", "enquiries", "courses", "attendance"]
for col in collections:
    db[col].drop()

# Clients
db.clients.insert_many([
    {
        "_id": "c001",
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "phone": "9876543210",
        "status": "active",
        "dob": "1990-07-01",
        "created_at": datetime(2024, 6, 1).isoformat()
    },
    {
        "_id": "c002",
        "name": "Amit Verma",
        "email": "amit@example.com",
        "phone": "9123456780",
        "status": "inactive",
        "dob": "1989-07-01",
        "created_at": datetime(2024, 5, 10).isoformat()
    },
    {
        "_id": "c003",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "1231231234",
        "status": "active",
        "dob": "1995-12-15",
        "created_at": datetime.now(UTC).isoformat()
    }
])

# Orders
db.orders.insert_many([
    {
        "order_id": "ORD001",
        "client_id": "c001",
        "service_name": "Yoga Beginner",
        "status": "pending",  # still due
        "amount": 3000,
        "created_at": datetime.now(UTC).isoformat()
    },
    {
        "order_id": "ORD002",
        "client_id": "c002",
        "service_name": "Zumba Pro",
        "status": "paid",
        "amount": 2500,
        "created_at": datetime.now(UTC).isoformat()
    },
    {
        "order_id": "ORD003",
        "client_id": "c003",
        "service_name": "Pilates Core",
        "status": "paid",
        "amount": 2000,
        "created_at": datetime.now(UTC).isoformat()
    }
])

# Payments
db.payments.insert_many([
    {
        "payment_id": "P001",
        "order_id": "ORD002",
        "paid": 2500,
        "paid_at": datetime.now(UTC).isoformat(),
        "method": "Credit Card"
    },
    {
        "payment_id": "P002",
        "order_id": "ORD001",
        "paid": 1000,
        "paid_at": datetime.now(UTC).isoformat(),
        "method": "UPI"
    },
    {
        "payment_id": "P003",
        "order_id": "ORD003",
        "paid": 2000,
        "paid_at": datetime.now(UTC).isoformat(),
        "method": "Net Banking"
    }
])

# Classes
today = datetime.today()
db.classes.insert_many([
    {
        "class_id": "CL001",
        "title": "Yoga Beginner",
        "start_time": (today + timedelta(days=1)).isoformat(),
        "instructor": "Rina Mehta",
        "status": "scheduled",
        "room": "Studio A"
    },
    {
        "class_id": "CL002",
        "title": "Zumba Pro",
        "start_time": (today + timedelta(days=3)).isoformat(),
        "instructor": "Karan Singh",
        "status": "scheduled",
        "room": "Studio B"
    },
    {
        "class_id": "CL003",
        "title": "Pilates Core",
        "start_time": (today - timedelta(days=2)).isoformat(),
        "instructor": "Rina Mehta",
        "status": "completed",
        "room": "Studio A"
    }
])

# Enquiries
db.enquiries.insert_many([
    {
        "enquiry_id": "ENQ001",
        "client_name": "Priya Sharma",
        "email": "priya@example.com",
        "phone": "9876543210",
        "status": "open",
        "created_at": datetime.now(UTC).isoformat()
    },
    {
        "enquiry_id": "ENQ002",
        "client_name": "Amit Verma",
        "email": "amit@example.com",
        "phone": "9123456780",
        "status": "closed",
        "created_at": datetime.now(UTC).isoformat()
    }
])

# Courses
db.courses.insert_many([
    {
        "course_id": "CR001",
        "title": "Yoga Beginner",
        "description": "A foundational course for yoga beginners",
        "category": "Yoga",
        "completion_rate": 80
    },
    {
        "course_id": "CR002",
        "title": "Pilates Core",
        "description": "Strength-focused pilates training",
        "category": "Pilates",
        "completion_rate": 65
    }
])

# Attendance
db.attendance.insert_many([
    {"client_id": "c001", "class": "Pilates", "present": True},
    {"client_id": "c001", "class": "Pilates", "present": False},
    {"client_id": "c002", "class": "Pilates", "present": False},
    {"client_id": "c003", "class": "Pilates", "present": True}
])

print("Sample data inserted successfully into MongoDB!")
