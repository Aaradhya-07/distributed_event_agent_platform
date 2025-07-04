# Distributed Event & Agent Platform

A high-performance, scalable distributed system built with Python that handles concurrent API requests and processes events asynchronously using Kafka, Celery, and PostgreSQL. Features real-time event processing with LLM integration for chemical research data enrichment.

## 🏗️ Architecture

This platform follows **Hexagonal Architecture** principles and consists of two microservices:

### Publisher Service
- **Purpose**: Receives API calls and publishes events to Kafka
- **Technology**: FastAPI, aiokafka
- **Port**: 8000

### Subscriber Service  
- **Purpose**: Consumes events from Kafka, processes them, and persists to database
- **Technology**: Celery, aiokafka, SQLAlchemy, PostgreSQL
- **Features**: LLM integration for chemical data enrichment

### Infrastructure
- **Message Broker**: Apache Kafka
- **Task Queue**: Celery with Redis
- **Database**: PostgreSQL
- **LLM Integration**: Groq API

## 📋 Prerequisites

- Python 3.8+
- Docker & Docker Compose
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd distributed_event_agent_platform
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```env
# Kafka
kafka_bootstrap_servers=localhost:9092
kafka_topic_user=user_events
kafka_topic_chemical=chemical_events

# PostgreSQL
postgres_url=postgresql+asyncpg://user:password@localhost:5432/db

# LLM (Groq)
llm_api_url=https://api.groq.com/v1/extract-properties
llm_api_key=YOUR_GROQ_API_KEY

# Celery Broker
celery_broker_url=redis://localhost:6379/0
```

### 3. Start Infrastructure
```bash
docker-compose up -d
```
This starts:
- Zookeeper (port 2181)
- Kafka (port 9092) 
- PostgreSQL (port 5432)
- Redis (port 6379)

### 4. Set Up Virtual Environments

#### Publisher Service
```bash
cd publisher-service
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pip install -e ../shared
```

#### Subscriber Service
```bash
cd subscriber-service
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pip install -e ../shared
```

### 5. Initialize Database
```bash
cd subscriber-service
python -m app.infrastructure.db_init
```

### 6. Start Services

#### Terminal 1: Publisher Service
```bash
cd publisher-service
venv\Scripts\activate
python run.py
```

#### Terminal 2: Celery Worker
```bash
cd subscriber-service
venv\Scripts\activate
python celery_worker.py worker --loglevel=info
```

#### Terminal 3: Kafka Consumer
```bash
cd subscriber-service
venv\Scripts\activate
python consumer_main.py
```

### 7. Test the System

1. **Access API Documentation**: http://localhost:8000/docs
2. **Test User Interaction Event**:
   ```json
   POST /events/user-interaction
   {
     "user_id": "user123",
     "event_type": "page_view",
     "timestamp": "2024-01-01T12:00:00",
     "event_metadata": {"page": "/home", "duration": 30}
   }
   ```

3. **Test Chemical Research Event**:
   ```json
   POST /events/chemical-research
   {
     "molecule_id": "mol123",
     "researcher": "Dr. Smith",
     "data": {"formula": "H2O", "weight": 18.015},
     "timestamp": "2024-01-01T12:00:00"
   }
   ```

## 📊 Monitoring

### Check Database
Connect to PostgreSQL:
- **Host**: localhost
- **Port**: 5432
- **User**: user
- **Password**: password
- **Database**: db

Tables:
- `user_interaction_events`
- `chemical_research_events`

### Check Logs
- **Publisher**: FastAPI logs in terminal
- **Celery**: Worker logs show task processing
- **Kafka Consumer**: Shows event dispatch

## 🏛️ Project Structure

```
distributed_event_agent_platform/
├── publisher-service/
│   ├── app/
│   │   ├── api/              # REST endpoints
│   │   │   ├── core/             # Business logic
│   │   │   ├── infrastructure/   # Kafka producer
│   │   │   └── main.py
│   │   ├── run.py
│   │   └── requirements.txt
│   ├── shared/                   # Common models, config
│   └── README.md
```

## 🔧 Configuration

### Environment Variables
All configuration is managed through environment variables or the `.env` file:

- `kafka_bootstrap_servers`: Kafka connection string
- `postgres_url`: PostgreSQL connection string
- `llm_api_url`: Groq API endpoint
- `llm_api_key`: Your Groq API key
- `celery_broker_url`: Redis connection for Celery

### Adding New Event Types
1. Add Pydantic model in `shared/models.py`
2. Add SQLAlchemy model in `shared/models.py`
3. Create API endpoint in `publisher-service/app/api/events.py`
4. Add Celery task in `subscriber-service/app/workers/event_handlers.py`
5. Update Kafka consumer in `subscriber-service/app/infrastructure/kafka_consumer_service.py`

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
If you see `ModuleNotFoundError: No module named 'shared'`:
```bash
# Make sure you're in the service directory with venv activated
pip install -e ../shared
```

#### Celery Permission Errors (Windows)
Windows-specific multiprocessing issues are normal. The system still works.

#### Kafka Connection Errors
Ensure Docker Compose is running:
```bash
docker-compose ps
```

#### Database Connection Errors
Check PostgreSQL is running and credentials are correct in `.env`.

## 🧪 Testing

### Manual Testing
1. Use the Swagger UI at http://localhost:8000/docs
2. Send test events and monitor logs
3. Check database for stored events

### API Endpoints
- `GET /health` - Health check
- `POST /events/user-interaction` - User analytics events
- `POST /events/chemical-research` - Chemical research events

## 🔄 Event Flow

1. **API Request** → Publisher Service
2. **Validation** → Pydantic models
3. **Publish** → Kafka topic
4. **Consume** → Kafka Consumer
5. **Process** → Celery task
6. **Enrich** → LLM (chemical events)
7. **Store** → PostgreSQL

## 🚀 Production Deployment

### Docker
Each service can be containerized:
```dockerfile
# Example for publisher service
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### Scaling
- **Publisher**: Multiple instances behind load balancer
- **Subscriber**: Multiple Celery workers
- **Kafka**: Multiple brokers
- **Database**: Read replicas

## 📝 License

[Your License Here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the logs for error details
