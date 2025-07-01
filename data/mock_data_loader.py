import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta

# Load env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Test connection
    db = client[MONGO_DB]
    print(f"✅ Connected to MongoDB Cloud: {MONGO_DB}")
except Exception as e:
    print("❌ Connection error:", e)
    exit()



# Drop old data (optional for fresh seed)
db.clients.drop()
db.orders.drop()
db.payments.drop()
db.classes.drop()
db.enquiries.drop()

# Insert into `clients`
db.clients.insert_many([
    {
        "_id": "c001",
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "phone": "9876543210"
    },
    {
        "_id": "c002",
        "name": "Amit Verma",
        "email": "amit@example.com",
        "phone": "9123456780"
    }
])

# Insert into `orders`
db.orders.insert_many([
    {
        "order_id": "ORD001",
        "client_id": "c001",
        "service_name": "Yoga Beginner",
        "status": "pending",
        "amount": 3000
    },
    {
        "order_id": "ORD002",
        "client_id": "c002",
        "service_name": "Zumba Pro",
        "status": "paid",
        "amount": 2500
    }
])

# Insert into `payments`
db.payments.insert_many([
    {
        "payment_id": "P001",
        "order_id": "ORD002",
        "paid": 2500
    },
    {
        "payment_id": "P002",
        "order_id": "ORD001",
        "paid": 1000
    }
])

# Insert into `classes`
today = datetime.today()
db.classes.insert_many([
    {
        "class_id": "CL001",
        "title": "Yoga Beginner",
        "start_time": (today + timedelta(days=1)).isoformat(),
        "instructor": "Rina Mehta",
        "status": "scheduled"
    },
    {
        "class_id": "CL002",
        "title": "Zumba Pro",
        "start_time": (today + timedelta(days=3)).isoformat(),
        "instructor": "Karan Singh",
        "status": "scheduled"
    },
    {
        "class_id": "CL003",
        "title": "Pilates Core",
        "start_time": (today - timedelta(days=2)).isoformat(),
        "instructor": "Rina Mehta",
        "status": "completed"
    }
])

# Insert into `enquiries`
db.enquiries.insert_many([
    {
        "enquiry_id": "ENQ001",
        "client_name": "Priya Sharma",
        "status": "open"
    },
    {
        "enquiry_id": "ENQ002",
        "client_name": "Amit Verma",
        "status": "closed"
    }
])

print("Sample data inserted successfully into MongoDB!")
