from aiokafka import AIOKafkaConsumer
from shared.config import Settings

class KafkaConsumer:
    def __init__(self, settings: Settings, topic: str, group_id: str):
        self.settings = settings
        self.topic = topic
        self.group_id = group_id
        self.consumer = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.settings.kafka_bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        await self.consumer.start()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def get_event(self):
        async for msg in self.consumer:
            yield msg.value 