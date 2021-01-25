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

## Good Practices
- Messages can be reused, however, usually in rpc, when you define a new rpc, you should create new request and response message types.
