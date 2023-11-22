import argparse

import asyncio
from loguru import logger

import grpc
import chat_pb2_grpc
import chat_pb2
from typing import List


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--chat", dest="chat", action="store_true", default=False, required=False
    )
    parser.add_argument(
        "-s",
        "--get-stats",
        dest="stat",
        action="store_true",
        default=False,
        required=False,
    )
    parser.add_argument(
        "-r",
        "--read-messages",
        dest="read",
        action="store_true",
        default=False,
        required=False,
    )
    return parser.parse_args()


def get_messages_from_user() -> List[chat_pb2.MessageRequest]:
    msgs = []
    while True:
        _msg = input("Write a message! Type 'done' to send!: ").strip()

        if _msg.lower() == "done":
            break

        msgs.append(chat_pb2.MessageRequest(message=_msg))
    return msgs


async def chat(stub: chat_pb2_grpc.ChatServiceStub) -> None:
    messages = stub.SendAndReceiveMessage(get_messages_from_user())
    async for message in messages:
        logger.info(f"Received message {message.message}")


async def stat(stub: chat_pb2_grpc.ChatServiceStub) -> None:
    stats = await stub.GetStats(chat_pb2.EmptyRequest())
    logger.info(f"Server has {stats.num_messages} messages")


async def read(stub: chat_pb2_grpc.ChatServiceStub) -> None:
    messages = stub.GetMessages(chat_pb2.EmptyRequest())
    async for message in messages:
        logger.info(f"Received message {message.message}")


async def main() -> None:
    args = parse_args()
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        if args.chat:
            await chat(stub)

        if args.stat:
            await stat(stub)

        if args.read:
            await read(stub)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
