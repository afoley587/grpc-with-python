# 1 Dollar DevOps: Building Your First gRPC-enabled Python App

## Introduction
Hey, fellow tech enthusiasts! Today, we're diving headfirst into the exciting 
world of gRPC – the not-so-secret sauce that's been causing a buzz in the 
software development scene. What's the deal with gRPC, you ask? Well, it's 
not your typical acronym; it stands for "gRPC Remote Procedure Call," and 
it's a game-changer when it comes to building distributed systems.

Imagine a toolkit, but not just any toolkit – one that redefines how we craft 
and connect pieces of software. That's gRPC for you, a brainchild of the folks 
at Google. Originally cooked up for Google's internal use, gRPC has since 
busted out of its corporate shell and gone open-source, becoming a go-to 
framework for developers in the know.

But what makes gRPC stand out? It's not your grandma's API. Instead of the 
usual RESTful approach, gRPC dances to the beat of the HTTP/2 protocol and 
grooves with Protocol Buffers (protobuf) for its interface language. The result? 
A lightweight, binary communication protocol that's not just fast but comes with 
cool features like bidirectional streaming and multiplexing. So, buckle up as 
we unravel the mysteries of gRPC, explore its nitty-gritty, and uncover how 
it's revolutionizing the game for developers.

## gRPC In Some More Depth
As previously noted, gRPC stands for "gRPC Remote Procedure Call" and is
essentially when a client calls a method directly on a server as if
it were a method on the client. For this to happen, the server needs to
implement an interface for the client to use and it needs to run a gRPC
server which can accept remote calls. The client provides "stubs" which 
can almost be thought of as mocked function versions of the functions
that the server provides in its interface.

These interfaces and stubs, along with the data structures they pass
between each other, are typically definted using Protocol Buffers
(Protobuf for short). We will be seeing protobufs in much more detail
as we do our code walkthrough, so for now, it is suffice to say that
we will define our services, remote procedure calls, and data structures
all with protobuf. We will then compile them using a special compiler,
and then use those in our source code on both the client and server.

So, what kind of calls does gRPC allow? We'll, its pretty flexible. 
We can define four different kinds of requests:

1. Simple RPC: A client sends a request to the server using the stub 
    and waits for a response to come back. This acts just as you would
    imagine a regular function call to work.
2. Response Streaming RPC: A client sends a request to the server 
    and gets a stream to read a sequence of messages back. The client 
    will keep reading messages from the server until an EOF is reached
    or the transport is closed. It helped me to think of this almost
    like a streaming response in HTTP. Yes, different mechanics, but
    the analogy is the same.
3. Request Streaming RPC: A client writes a sequence of messages and 
    sends them to the server. Similar to the above, but in the reverse
    order. The server will keep reading the input messages, perform
    some action on them, and then give a response when it is done 
    processing.
4. Bidirectionally Streaming RPC: Both client and server send a 
    sequence of messages using a read-write stream. The sides of the
    stream are independent. So server writes don't conflict with client
    writes and vice-versa. Personally, I find this RPC the most
    interesting and we are going to use it today to build our 
    project.

## The Project
Today, we will be building a bi-directional chat system utilizing gRPC.
We see this project all of the time with websockets - where users connect
to a websocket and chats are broadcast to the entire chat room - but we
just want to see if we can build the same system without websockets. Note
that this really isn't a blog post about "HOW TO BUILD A CHAT ROOM SYSTEM!!!"
but more of a blog post about "Dipping your toes into gRPC with python".

Our system will have three methods:
1. A method to send more chats to the server. In this case, we will
    have a bi-directional channel so that the client can send messages
    while simultaneously retrieving them from the server as well. For 
    each message the server receives, it will send back an acknowledgement
    over it's side of the channel as the client keeps sending more.
2. A method to see how many messages have been sent to the server. In this 
    case, we can implement a simple RPC. We can do pretty much a point and 
    shoot thing here where we ask the server how many messages its read and
    it can respond with the actual number.
3. A method to read all of the messages from the server. In this case,
    we can implement a response streaming RPC. We can request all of the
    messages from the server, and it can send them one by one over the channel.

## Part I: The Protobuf
Let's first go through the protocol buffers which will define our service 
interface and all data structures that will pass through our interface.

First, the service:

```proto
// Defines our service interface with methods
service ChatService {
  // Get high level stats from the server
  rpc GetStats(EmptyRequest) returns (StatsReply) {}
  // Stream the current messages from the server
  rpc GetMessages(EmptyRequest) returns (stream MessageReply) {}
  // Sends and receives chat messages bi-directionally
  rpc SendAndReceiveMessage (stream MessageRequest) returns (stream MessageReply) {}
}
```

As we can see, we have three methods in our service. These each correlate
to the methods we discussed in the previous section. We see that
our `GetStats` method takes an `EmptyRequest` as a parameter and returns
a `StatsReply` response. You'll notice the word `stream` isn't anywhere
in this method signature, so it's a simple RPC. There isn't any streaming
on this method. Next, we see the `GetMessages` method takes an `EmptyRequest`
and returns a stream of `MessageReply`. Meaning that this method will write
each message onto the channel as the server processes them. This is an example
of a Response Streaming RPC. Finally, we have the `SendAndReceiveMessage`
method which accepts a stream of `MessageRequest` and responds with a stream
of `MessageReply`. So, both the client and the server can simultaneously read
and write on to their respective channels. Fun!

We next define our message structures:

```proto
// This is the request we will send to our server. We will
// accept a user who the message is coming from, which
// chat room it is in, and the message to send
message MessageRequest {
  string user_from = 1;
  string chat_room = 2;
  string message = 3;
}

// This is the reply we will get back from our server. We will
// expect a user who the message is coming from, which
// chat room it is in, and the message to send
message MessageReply {
  string user_from = 1;
  string chat_room = 2;
  string message = 3;
}

// An empty request for requesting messages or
// stats from the server
message EmptyRequest {}

// A statis request from the server
message StatsReply {
  int32 num_messages = 1;
}
```

We have four message structures:
1. `MessageRequest` - A message to be sent to the server with
    a username, chat room name, and a message
2. `MessageReply`- A message acknowledgement to be sent from the server 
    with a username, chat room name, and a message
3. `EmptyRequest` - A generic empty request
4. `StatsReply` - A stat's reply message with an integer number of messages

Note that in a production system, you likely wouldn't want to use a generic
empty request as it makes decoupling your code a bit harder when you want
to make changes.

We can compile our protocol buffers using the python library, `grpc_tools`.
In the most basic form, we can run something like the below:

```shell
python -m grpc_tools.protoc \
    -I/path/to/protobuf/imports \
    --python_out=/path/to/python/directory \
    --pyi_out=/path/to/python/directory \
    --grpc_python_out=/path/to/python/directory \
    /path/to/proto/file
```

And in our file structure:
```shell
python -m grpc_tools.protoc \
    -I../protos \
    --python_out=. \
    --pyi_out=. \
    --grpc_python_out=. \
    ../protos/chat.proto

```

If you list your python directory, you would see three new files:
* `chat_pb2_grpc.py` - Your service classes and client stubs
* `chat_pb2.py` - Your exported message structures
* `chat_pb2.pyi` - The python interfaces of the message structures

## Part II: The Server
We can now walk through the server-side of our code. From a high level,
we will need a new python class which implements our protobuf service and
then a method to attach the service to a server and run it until completion.

Let's start with the service:

```python
import grpc
from typing import AsyncIterable, List
from loguru import logger
import asyncio

import chat_pb2_grpc
import chat_pb2


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    """Provides methods that implement functionality of chat server."""

    def __init__(self):
        self.messages_received: List[chat_pb2.MessageRequest] = []

    async def GetStats(
        self, request: chat_pb2.EmptyRequest, unused_context
    ) -> chat_pb2.StatsReply:
        return chat_pb2.StatsReply(num_messages=len(self.messages_received))

    async def GetMessages(
        self, request: chat_pb2.EmptyRequest, unused_context
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
```

Most of the imports seem standard, but what are these two lines:

```python
import chat_pb2_grpc
import chat_pb2
```

Well, they are the generate python files from our protobuf! How cool!
We see that our `ChatServiceServicer` class inherits from the service
defined in the `chat_pb2_grpc` file. 

The methods in the service should look extremely familiar because, again,
they were defined in our protobuf files. Let's break them down one-by-one.

`GetStats` accepts a request of type `EmptyRequest`. It then counts the
number of messages it has in memory and returns a `StatsReply` with
that number of messages.

`GetMessages` accepts a request of type `EmptyRequest`. It then loops 
through the messages it has seen before and to puts them on 
the stream. Note that this methoud returns an `AsyncIterable`, so the client 
will do an `async for ...` over the response from this method.

`SendAndReceiveMessage` accepts a request of 
`AsyncIterable[chat_pb2.MessageRequest]`. So our client would call this 
method with multiple messages. The server would then go through the messages
asyncronously and acknowledge it with a response of type `MessageReply`. This,
again, returns an `AsyncIterable`.

Finally, we need a way to run the server! Let's define a `serve` method:

```python
async def serve() -> None:
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()
```

So we first create a server with gRPC IO calls. Then, we add the chat
service to the server and start the server.

We can run this with `python server.py`.

## Part III: The Client