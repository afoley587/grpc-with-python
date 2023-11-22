import grpc
from typing import AsyncIterable
from loguru import logger
import asyncio

import chat_pb2_grpc
import chat_pb2


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.messages_received: AsyncIterable[chat_pb2.MessageRequest] = []

    async def GetStats(
        self, request: chat_pb2.StatsRequest, unused_context
    ) -> chat_pb2.StatsReply:
        return chat_pb2.StatsReply(num_messages=len(self.messages_received))

    async def GetMessages(
        self, request: chat_pb2.StatsRequest, unused_context
    ) -> AsyncIterable[chat_pb2.MessageReply]:
        for msg in self.messages_received:
            yield msg

    async def SendAndReceiveMessage(
        self,
        request_iterator: AsyncIterable[chat_pb2.MessageRequest],
        unused_context,
    ) -> AsyncIterable[chat_pb2.MessageReply]:
        async for new_msg in request_iterator:
            self.messages_received.append(new_msg)
            resp = chat_pb2.MessageReply(
                message=f"Server Responding to {new_msg.message}",
                user_from="server",
                chat_room=new_msg.chat_room,
            )
            logger.info(f"Server side got: {new_msg.message} in {new_msg.chat_room}")
            yield resp


async def serve() -> None:
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(serve())
