from aiokafka import AIOKafkaConsumer
from shared.config import Settings

class KafkaConsumer:
    """KafkaConsumer abstraction for consuming messages from Kafka topics."""
    def __init__(self, settings: Settings, topic: str, group_id: str):
        """Initialize the KafkaConsumer with settings, topic, and group ID."""
        self.settings = settings
        self.topic = topic
        self.group_id = group_id
        self.consumer = None

    async def start(self):
        """Start the Kafka consumer connection and subscribe to the topic."""
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.settings.kafka_bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        await self.consumer.start()

    async def stop(self):
        """Stop the Kafka consumer connection."""
        if self.consumer:
            await self.consumer.stop()

    async def get_event(self):
        """Asynchronously yield messages from the Kafka topic."""
        async for msg in self.consumer:
            yield msg.value 