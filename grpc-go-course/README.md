## Server Streaming API

* Server Streaming RPC API are a NEW kind API enabled thanks to HTTP/2
* The client will send one message to the server and will receive many responses from the server, possibly an infinite number.
* Streaming server are well suited for:
  - when the server needs to send a LOT of data (big data)
  - when the server needs to "PUSH" data to the client without having the client request for more (e.g. live feed, chat, etc.)

```
              Server Streaming API
************                               ************
*          * -------> req 0 -------------> *          *
*  client  *                               *  server  *
*          * <-- resp 0, 1, 2, 3, ... <--- *          *
************                               ************
```

* in gRPC Server Streaming Calls are defined using the keyword "stream"


### Good Practices
- Messages can be reused, however, usually in rpc, when you define a new rpc, you should create new request and response message types.
