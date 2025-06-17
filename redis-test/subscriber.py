# This is a simpler script than the publisher. It does not need FastAPI.
# Like the publisher, it will use the redis-py library to connect to the Redis service \
    # at the hostname redis.
# You will create a "pubsub" object from your Redis connection \
    # and subscribe() it to the exact same channel name you used in the publisher (e.g., my-channel).
# You will then create an infinite loop that "listens" for messages on that channel. \
    # When a message is received, the script will print its contents to the console.

import os
import sys
import asyncio
import redis.asyncio as redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

REDIS_CHANNEL = "fastapi_channel"

async def main():
    while True:
        try:
            redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
            await redis_client.ping()
            print(f"Successfully connected to Redis at {REDIS_HOST}:{REDIS_PORT}.")
            pubsub = redis_client.pubsub()
            await pubsub.subscribe(REDIS_CHANNEL)
            print(f"Subscribed to channel: '{REDIS_CHANNEL}'. Listening for messages...")
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    print(f"Received Message: {message['data']}")
        except redis.ConnectionError:
            print(f"Connection to Redis lost. Retrying in 5 seconds...", file=sys.stderr)
            await asyncio.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            print("Shutting down subscriber.", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSubscriber stopped by user.")
        sys.exit(0)