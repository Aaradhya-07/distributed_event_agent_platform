from aiokafka import AIOKafkaProducer
from shared.config import Settings

class KafkaProducer:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.settings.kafka_bootstrap_servers
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send(self, topic: str, value: bytes):
        await self.producer.send_and_wait(topic, value) 