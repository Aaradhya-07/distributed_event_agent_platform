import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.infrastructure.kafka_consumer_service import KafkaConsumerService

async def main():
    consumer_service = KafkaConsumerService()
    try:
        print("Starting Kafka consumer service...")
        await consumer_service.start()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await consumer_service.stop()

if __name__ == "__main__":
    asyncio.run(main()) 