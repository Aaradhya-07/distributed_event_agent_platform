from fastapi import APIRouter, HTTPException, status, Depends
from shared.models import UserInteractionEvent, ChemicalResearchEvent
from shared.config import Settings
from ..infrastructure.kafka_producer import KafkaProducer
import json

router = APIRouter()

# Dependency to get KafkaProducer instance
def get_kafka_producer():
    """Dependency to provide a KafkaProducer instance with loaded settings."""
    settings = Settings()
    return KafkaProducer(settings)

@router.post("/user-interaction", status_code=status.HTTP_202_ACCEPTED)
async def publish_user_interaction(
    event: UserInteractionEvent,
    producer: KafkaProducer = Depends(get_kafka_producer)
):
    """Publish a user interaction event to Kafka.
    Args:
        event: The user interaction event payload.
        producer: KafkaProducer dependency.
    Returns:
        Success message.
    """
    await producer.start()
    try:
        # Send the event to the user events Kafka topic
        await producer.send(
            topic=Settings().kafka_topic_user,
            value=event.json().encode("utf-8")
        )
    finally:
        await producer.stop()
    return {"message": "User interaction event published."}

@router.post("/chemical-research", status_code=status.HTTP_202_ACCEPTED)
async def publish_chemical_research(
    event: ChemicalResearchEvent,
    producer: KafkaProducer = Depends(get_kafka_producer)
):
    """Publish a chemical research event to Kafka.
    Args:
        event: The chemical research event payload.
        producer: KafkaProducer dependency.
    Returns:
        Success message.
    """
    await producer.start()
    try:
        # Send the event to the chemical events Kafka topic
        await producer.send(
            topic=Settings().kafka_topic_chemical,
            value=event.json().encode("utf-8")
        )
    finally:
        await producer.stop()
    return {"message": "Chemical research event published."} 