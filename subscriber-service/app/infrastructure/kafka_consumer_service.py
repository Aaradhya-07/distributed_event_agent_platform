import asyncio
import json
from aiokafka import AIOKafkaConsumer
from shared.config import Settings
from app.workers.event_handlers import process_user_event, process_chemical_event

class KafkaConsumerService:
    def __init__(self):
        self.settings = Settings()
        self.consumers = []
        
    async def start(self):
        # Create consumers for both topics
        user_consumer = AIOKafkaConsumer(
            self.settings.kafka_topic_user,
            bootstrap_servers=self.settings.kafka_bootstrap_servers,
            group_id='user_event_processor',
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        
        chemical_consumer = AIOKafkaConsumer(
            self.settings.kafka_topic_chemical,
            bootstrap_servers=self.settings.kafka_bootstrap_servers,
            group_id='chemical_event_processor',
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        
        self.consumers = [user_consumer, chemical_consumer]
        
        # Start all consumers
        for consumer in self.consumers:
            await consumer.start()
            
        # Start processing tasks
        await asyncio.gather(
            self._process_user_events(user_consumer),
            self._process_chemical_events(chemical_consumer)
        )
    
    async def _process_user_events(self, consumer):
        async for msg in consumer:
            try:
                event_data = msg.value.decode('utf-8')
                process_user_event.delay(event_data)
                print(f"User event dispatched: {event_data[:100]}...")
            except Exception as e:
                print(f"Error processing user event: {e}")
    
    async def _process_chemical_events(self, consumer):
        async for msg in consumer:
            try:
                event_data = msg.value.decode('utf-8')
                process_chemical_event.delay(event_data)
                print(f"Chemical event dispatched: {event_data[:100]}...")
            except Exception as e:
                print(f"Error processing chemical event: {e}")
    
    async def stop(self):
        for consumer in self.consumers:
            await consumer.stop() 