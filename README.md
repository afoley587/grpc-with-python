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

## Part II: The Server

## Part III: The Client