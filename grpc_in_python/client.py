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


def get_messages_from_user(user: str, chat_room: str) -> List[chat_pb2.MessageRequest]:
    msgs = []
    while True:
        _msg = input("Write a message! Type 'done' to send!: ").strip()

        if _msg.lower() == "done":
            break

        msgs.append(
            chat_pb2.MessageRequest(user_from=user, chat_room=chat_room, message=_msg)
        )
    return msgs


async def chat(stub: chat_pb2_grpc.ChatServiceStub, user: str, chat_room: str) -> None:
    # gRPC AsyncIO bidi-streaming RPC API accepts both synchronous iterables
    # and async iterables.
    call = stub.SendAndReceiveMessage(get_messages_from_user(user, chat_room))
    async for response in call:
        logger.info(f"Received message {response.message} in {response.chat_room}")


async def stat(stub: chat_pb2_grpc.ChatServiceStub, user: str, chat_room: str) -> None:
    # gRPC AsyncIO bidi-streaming RPC API accepts both synchronous iterables
    # and async iterables.
    request = chat_pb2.EmptyRequest()
    stats = await stub.GetStats(request)
    logger.info(f"Server has {stats.num_messages} messages")


async def read(stub: chat_pb2_grpc.ChatServiceStub, user: str, chat_room: str) -> None:
    # gRPC AsyncIO bidi-streaming RPC API accepts both synchronous iterables
    # and async iterables.
    request = chat_pb2.EmptyRequest()
    call = stub.GetMessages(request)
    async for response in call:
        logger.info(f"Received message {response.message} in {response.chat_room}")


async def main() -> None:
    args = parse_args()

    # if args.send_chat
    # if args.get_stats
    # if args.read_all_messages
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        if args.chat:
            await chat(stub, "test_user", "test_room")

        if args.stat:
            await stat(stub, "test_user", "test_room")

        if args.read:
            await read(stub, "test_user", "test_room")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
