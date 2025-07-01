             ┌──────────────────────┐
             │  User (Prompt Input) │
             └─────────┬────────────┘
                       │
                       ▼
             ┌──────────────────────┐
             │   FastAPI Backend    │
             │  /support-agent/query│
             │ /dashboard-agent/query
             └─────────┬────────────┘
                       │
         ┌─────────────┴──────────────┐
         │                            │
         ▼                            ▼
┌────────────────────┐     ┌──────────────────────┐
│   Support Agent     │     │   Dashboard Agent     │
└────────┬────────────┘     └────────┬──────────────┘
         │                           │
         ▼                           ▼
┌───────────────┐         ┌────────────────────┐
│ Natural Prompt│         │   Analytics Engine │
│ Understanding │         └──────────┬─────────┘
└───────┬───────┘                    │
        │                            ▼
        ▼                ┌────────────────────────────┐
┌──────────────────────┐ │ MongoDBTool (Read & Aggreg)│
│ ExternalAPITool      │ └────────────────────────────┘
│ (for Create APIs)    │
└────────┬─────────────┘
         ▼
┌──────────────────────┐
│ MongoDB Collections  │
│ (clients, orders,    │
│  payments, courses,  │
│  classes, attendance)│
└──────────────────────┘
