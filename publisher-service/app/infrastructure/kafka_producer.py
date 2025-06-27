from aiokafka import AIOKafkaProducer
from shared.config import Settings

class KafkaProducer:
    """KafkaProducer abstracts the aiokafka producer functionality."""
    def __init__(self, settings: Settings):
        """Initialize the KafkaProducer with settings."""
        self.settings = settings
        self.producer = None

    async def start(self):
        """Start the Kafka producer connection."""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.settings.kafka_bootstrap_servers
        )
        await self.producer.start()

    async def stop(self):
        """Stop the Kafka producer connection."""
        if self.producer:
            await self.producer.stop()

    async def send(self, topic: str, value: bytes):
        """Send a message to the specified Kafka topic.
        Args:
            topic: Kafka topic name.
            value: Message payload as bytes.
        """
        await self.producer.send_and_wait(topic, value) 