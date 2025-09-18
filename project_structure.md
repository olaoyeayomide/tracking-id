FULL STRUCTURE

tracking-id/
│── backend/
│ ├── app/
│ │ ├── **init**.py
│ │ ├── main.py # FastAPI entry point
│ │ ├── core/ # Core settings & utilities
│ │ │ ├── config.py # App settings, env configs
│ │ │ ├── security.py # Auth, API keys, rate limiting
│ │ │ └── logger.py # Logging config
│ │ ├── database/
│ │ │ ├── **init**.py
│ │ │ ├── connection.py # Database session setup
│ │ │ └── models/ # SQLAlchemy models
│ │ │ ├── **init**.py
│ │ │ ├── user.py
│ │ │ ├── carrier.py
│ │ │ ├── shipment.py
│ │ │ └── tracking_event.py
│ │ ├── schemas/ # Pydantic models
│ │ │ ├── **init**.py
│ │ │ ├── user_schema.py
│ │ │ ├── carrier_schema.py
│ │ │ └── tracking_schema.py
│ │ ├── routers/ # API routes
│ │ │ ├── **init**.py
│ │ │ ├── auth.py
│ │ │ ├── users.py
│ │ │ ├── carriers.py
│ │ │ ├── tracking.py
│ │ │ └── webhooks.py
│ │ ├── services/ # Business logic
│ │ │ ├── **init**.py
│ │ │ ├── carrier_connector/ # Carrier integrations
│ │ │ │ ├── **init**.py
│ │ │ │ ├── gig.py
│ │ │ │ ├── kwik.py
│ │ │ │ ├── nipost_scraper.py
│ │ │ │ └── dhl.py
│ │ │ ├── normalizer.py # Normalize carrier data
│ │ │ ├── tracker.py # Shipment tracking logic
│ │ │ └── notifier.py # Email/SMS notifications
│ │ ├── utils/ # Helpers
│ │ │ ├── **init**.py
│ │ │ ├── scraper.py
│ │ │ ├── parsers.py
│ │ │ └── validators.py
│ │ └── tests/ # Unit & integration tests
│ │ ├── **init**.py
│ │ ├── test_auth.py
│ │ ├── test_tracking.py
│ │ └── test_carrier_connector.py
│ ├── requirements.txt
│ └── alembic/ # DB migrations

│── frontend/ # If building frontend (React, Vue, or Next.js)
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ ├── pages/
│ │ ├── services/ # API calls to backend
│ │ └── styles/
│ └── package.json

│── docs/ # Documentation
│ ├── architecture.md
│ ├── api_reference.md
│ └── carrier_notes.md

│── .env # Environment variables
│── .gitignore
│── docker-compose.yml # Optional: container setup
│── README.md

PHASE ONE

tracking-id/
│── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── core/config.py
│ │ ├── database/connection.py
│ │ ├── database/models/
│ │ │ ├── user.py
│ │ │ └── shipment.py
│ │ ├── schemas/tracking_schema.py
│ │ ├── routers/tracking.py
│ │ └── services/carrier_connector/
│ │ ├── gig.py
│ │ └── dhl.py
│ ├── requirements.txt
│ └── alembic/
│── docs/architecture.md
│── .env
│── README.md
