# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_pb2 as chat__pb2


class ChatServiceStub(object):
    """option objc_class_prefix = "CHAT";

    Defines our service interface with methods
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetStats = channel.unary_unary(
            "/grpc.chat.ChatService/GetStats",
            request_serializer=chat__pb2.EmptyRequest.SerializeToString,
            response_deserializer=chat__pb2.StatsReply.FromString,
        )
        self.GetMessages = channel.unary_stream(
            "/grpc.chat.ChatService/GetMessages",
            request_serializer=chat__pb2.EmptyRequest.SerializeToString,
            response_deserializer=chat__pb2.MessageReply.FromString,
        )
        self.SendAndReceiveMessage = channel.stream_stream(
            "/grpc.chat.ChatService/SendAndReceiveMessage",
            request_serializer=chat__pb2.MessageRequest.SerializeToString,
            response_deserializer=chat__pb2.MessageReply.FromString,
        )


class ChatServiceServicer(object):
    """option objc_class_prefix = "CHAT";

    Defines our service interface with methods
    """

    def GetStats(self, request, context):
        """Get high level stats from the server"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetMessages(self, request, context):
        """Stream the current messages from the server"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def SendAndReceiveMessage(self, request_iterator, context):
        """Sends and receives chat messages bi-directionally"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ChatServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetStats": grpc.unary_unary_rpc_method_handler(
            servicer.GetStats,
            request_deserializer=chat__pb2.EmptyRequest.FromString,
            response_serializer=chat__pb2.StatsReply.SerializeToString,
        ),
        "GetMessages": grpc.unary_stream_rpc_method_handler(
            servicer.GetMessages,
            request_deserializer=chat__pb2.EmptyRequest.FromString,
            response_serializer=chat__pb2.MessageReply.SerializeToString,
        ),
        "SendAndReceiveMessage": grpc.stream_stream_rpc_method_handler(
            servicer.SendAndReceiveMessage,
            request_deserializer=chat__pb2.MessageRequest.FromString,
            response_serializer=chat__pb2.MessageReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "grpc.chat.ChatService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class ChatService(object):
    """option objc_class_prefix = "CHAT";

    Defines our service interface with methods
    """

    @staticmethod
    def GetStats(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/grpc.chat.ChatService/GetStats",
            chat__pb2.EmptyRequest.SerializeToString,
            chat__pb2.StatsReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetMessages(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/grpc.chat.ChatService/GetMessages",
            chat__pb2.EmptyRequest.SerializeToString,
            chat__pb2.MessageReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def SendAndReceiveMessage(
        request_iterator,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            "/grpc.chat.ChatService/SendAndReceiveMessage",
            chat__pb2.MessageRequest.SerializeToString,
            chat__pb2.MessageReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
