## Server Streaming API

* Server Streaming RPC API are a NEW kind API enabled thanks to HTTP/2
* The client will send one message to the server and will receive many responses from the server, possibly an infinite number.
* Streaming server are well suited for:
  - when the server needs to send a LOT of data (big data)
  - when the server needs to "PUSH" data to the client without having the client request for more (e.g. live feed, chat, etc.)
* in gRPC Server Streaming Calls are defined using the keyword `stream`

```
              Server Streaming API
************                               ************
*          * -------> req 0 -------------> *          *
*  client  *                               *  server  *
*          * <-- resp 0, 1, 2, 3, ... <--- *          *
************                               ************
```

## Client Streaming API

* Client Streaming RPC API are a NEW kind API enabled thanks to HTTP/2
* The client will send **many messages** to the server and will receive **one response** from the server (at any time)
* Streaming Client are well suited for:
  - When the client needs to send a lot of data (big data)
  - When the server processing is expensive and should happen as the client sends data
  - When the client needs to "PUSH" data to the server without really expecting a response
* in gRPC Server Streaming Calls are defined using the keyword `stream`

```
              Client Streaming API
************                               ************
*          * --> req ..., 3, 2, 1, 0 ----> *          *
*  client  *                               *  server  *
*          * <-- resp 0 <----------------- *          *
************                               ************
```

## Bi-Directional Streaming API

* Bi-Directional Streaming RPC API are a NEW kind API enabled thanks to HTTP/2
* The client will send **many messages** to the server and will receive **many responses** from the server
* **The number of requests and responses does not have to match**
* Bi-Directional Streaming RPC are well suited for:
  - When the client and the server needs to send a lot of data asynchronously
  - "Chat" protocol
  - Long running connections
* In gRPC, Bi Directional Streaming API are defined using the keyword `stream`, **twice**

```
              Bi-Directional Streaming API
************                               ************
*          * --> req ..., 3, 2, 1, 0 ----> *          *
*  client  *                               *  server  *
*          * <-- resp 0, 1, 2, 3, ... <--- *          *
************                               ************

```

### Deadlines
* Deadlines allow gRPC clients to specify how long they are willing to wait for an RPC to complete before the RPC is terminated with the error `DEADLINE_EXCEEDED`
* The gRPC documentation recommends you set a deadline for ALL client RPC calls
* Setting the deadline is up to you: how long do you feel your API should have to complete?
  - usually small APIs: 100 ms, 500 ms, or 1000 ms (if slower response is okay)
  - for long API call: 5 min?
  - etc... up to you.
* The server should check if the deadline has exceeded and cancel the work it is doing.
* **NOTE**: Deadlines are propagated across if gRPC alls are chained. For example:
  - A => B => C (deadline for A is passed to B and then passed to C)
  - Hence, C would be "aware" of the deadline of the client A...


## Good Practices
- Messages can be reused, however, usually in rpc, when you define a new rpc, you should create new request and response message types.
