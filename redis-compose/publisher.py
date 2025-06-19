# Use the FastAPI library to create a web application.
# Define a single endpoint using a POST request at the path /publish. \
    # POST is used because the client is sending data (the message to publish) to the server.
# Use a Python Redis client library (like redis-py) to establish a connection to your Redis service.
    # The host for this connection will be redis \
    # (the name you gave the Redis service in your docker-compose.yml file).
# In your /publish endpoint function, you will take the message from the request body \
    # and use the Redis client to publish() it to a specific channel \
    # (e.g., you can name the channel my-channel).

import os
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

REDIS_CHANNEL = "fastapi_channel"

class Message(BaseModel):
    message: str

app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: attempting to connect to Redis...")
    try:
        redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
        await redis_client.ping()
        app_state["redis_client"] = redis_client
        print("Successfully connected to Redis.")
    except redis.ConnectionError as e:
        print(f"FATAL: Could not connect to Redis. Error: {e}")
        app_state["redis_client"] = None
    yield
    print("Application shutdown: closing Redis connection...")
    redis_client = app_state.get("redis_client")
    if redis_client:
        await redis_client.close()
        print("Redis connection closed.")

app = FastAPI(
    lifespan=lifespan,
    title="Redis Publisher API",
    description="An API to publish messages to a Redis channel.",
    version="1.0.0"
)

@app.post("/publish", status_code=200)
async def publish_message(item: Message):
    redis_client = app_state.get("redis_client")
    if not redis_client:
        raise HTTPException(
            status_code=503,
            detail="Cannot publish message: Redis service is unavailable."
        )
    try:
        subscriber_count = await redis_client.publish(REDIS_CHANNEL, item.message)
        return {
            "status": "success",
            "published_to_channel": REDIS_CHANNEL,
            "message_sent": item.message,
            "subscribers_received": subscriber_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while publishing: {e}"
        )

# This part is for convenience. It allows you to run 'python publisher.py'
# to test the app locally without needing Docker, but the primary way to run
# this service for the assignment is with 'docker-compose up'.
# The command would be: uvicorn publisher:app --reload