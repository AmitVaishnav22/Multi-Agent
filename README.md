#  Multi-Agent Backend System (Support + Dashboard Agents)

This is a FastAPI-based multi-agent backend system powered by MongoDB and Python. It features two intelligent agents:

1. **SupportAgent**: Handles service-related queries
2. **DashboardAgent**: Handles business analytics and metrics

Agents process user prompts and intelligently fetch or modify data using MongoDB and simulated external APIs.

---

## Architecture
```mermaid
graph LR
    A[User Prompt] --> B{Router (/query)}
    B --> C[SupportAgent]
    B --> D[DashboardAgent]
    C --> E[MongoDBTool + ExternalAPI]
    D --> F[MongoDBTool (Aggregations)]
    E --> G[(MongoDB)]
    F --> G
```

---

## 🚀Tech Stack

| Category      | Tools Used                  |
| ------------- | --------------------------- |
| Language      | Python 3.10+                |
| Framework     | FastAPI                     |
| Database      | MongoDB Atlas               |
| Agent Logic   | Custom Python Classes       |
| External APIs | Mock External Service Calls |
| Deployment    | Local / Docker-ready        |

---

## Agents Overview

### Support Agent

Handles client-facing tasks:

* View client details
* Check order/payment status
* View classes & courses
* Create new orders or enquiries

### Dashboard Agent

Provides business analytics:

* Total revenue
* Outstanding payments
* Client insights (active/inactive, birthdays)
* Service trends
* Attendance stats

---

## MongoDB Collections

* `clients`: Registered users
* `orders`: Service orders
* `payments`: Payment history
* `classes`: Upcoming/completed classes
* `courses`: Course metadata
* `attendance`: Class attendance logs
* `enquiries`: Client enquiry tracking

---

## Project Structure

```
multi-agent-backend/
├── agents/
│   ├── support_agent.py
│   └── dashboard_agent.py
├── tools/
│   ├── mongodb_tool.py
│   └── external_api_tool.py
├── data/
│   └── mock_data_loader.py
├── services/
│   └── query_router.py
├── main.py
├── requirements.txt
└── README.md
```

---

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up `.env`

```env
MONGO_URI=<your-mongodb-uri>
MONGO_DB=multi_agent_db
```

### 3. Load Mock Data

```bash
python data/mock_data_loader.py
```

### 4. Run FastAPI Server

```bash
uvicorn main:app --reload
```

### 5. Test with cURL or Postman

```http
POST /query
{
  "prompt": "Has order #ORD002 been paid?"
}
```

---

<!-- ## Bonus Features (Coming Soon)

* [ ] Multilingual query support (e.g., Hindi, French)
* [ ] Session memory for recent context
* [ ] RAG-based smart answering (GPT + Mongo) -->

---

## Sample Prompts

### Support Agent:

* "Create an order for Zumba Pro for Amit Verma"
* "What classes are available this week?"
* "Has order #ORD001 been paid?"

### Dashboard Agent:

* "How much revenue did we generate this month?"
* "What is the attendance percentage for Pilates?"
* "How many inactive clients do we have?"

---

## Author

**Amit Vaishnav**

> Built with real-world architecture, smart routing, and MongoDB logic to simulate an intelligent backend system.

---

## License

MIT License

