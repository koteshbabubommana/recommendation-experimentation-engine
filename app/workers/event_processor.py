import asyncio
from app.utils.logger import logger


async def process_event_async(event: dict):
    await asyncio.sleep(0.05)

    logger.info("Processed event asynchronously: %s", event)

    return {
        "status": "processed",
        "event": event
    }