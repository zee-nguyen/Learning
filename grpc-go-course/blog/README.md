# Session 10: [Hands-On] CRUD API with MongoDB

---

## 51. Instal MongoDB

### 51.1. gRPC CRUD with MongoDB

* section overview:
  * we'll implement a "blog" service in which we'll
    * Create
    * Read
    * Update
    * Delete
  * blogs, using [MongoDB](https://www.mongodb.com/) as a backend
  * No MongoDB knowledge is needed for this section
  * You could replace MongoDB by your favourite database as an exercise

* MongoDB Community Server: [link](https://www.mongodb.com/download-center/community)
* MongoDB MacOS installation: [docs](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

Shortly, let's do this command:

```bash
brew tap mongodb/brew
brew install mongodb-community@4.2
```

run `mongod`

```bash
$ mongod
2020-03-30T00:41:03.430+0900 I  CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2020-03-30T00:41:03.433+0900 I  CONTROL  [initandlisten] MongoDB starting : pid=55207 port=27017 dbpath=/data/db 64-bit host=Marks-MacBook-Pro.local
2020-03-30T00:41:03.433+0900 I  CONTROL  [initandlisten] db version v4.2.3
2020-03-30T00:41:03.433+0900 I  CONTROL  [initandlisten] git version: 6874650b362138df74be53d366bbefc321ea32d4
2020-03-30T00:41:03.433+0900 I  CONTROL  [initandlisten] allocator: system
2020-03-30T00:41:03.433+0900 I  CONTROL  [initandlisten] modules: none
2020-03-30T00:41:03.433+0900 I  CONTROL  [initandlisten] build environment:
2020-03-30T00:41:03.433+0900 I  CONTROL  [initandlisten]     distarch: x86_64
2020-03-30T00:41:03.433+0900 I  CONTROL  [initandlisten]     target_arch: x86_64
2020-03-30T00:41:03.433+0900 I  CONTROL  [initandlisten] options: {}
2020-03-30T00:41:03.434+0900 I  STORAGE  [initandlisten] exception in initAndListen: NonExistentPath: Data directory /data/db not found., terminating
2020-03-30T00:41:03.434+0900 I  NETWORK  [initandlisten] shutdown: going to close listening sockets...
2020-03-30T00:41:03.434+0900 I  -        [initandlisten] Stopping further Flow Control ticket acquisitions.
2020-03-30T00:41:03.434+0900 I  CONTROL  [initandlisten] now exiting
2020-03-30T00:41:03.434+0900 I  CONTROL  [initandlisten] shutting down with code:100
```

and we got some errors:

```bash
2020-03-30T00:41:03.434+0900 I  STORAGE  [initandlisten] exception in initAndListen: NonExistentPath: Data directory /data/db not found., terminating
```

this means that `mongodb` cannot find the Data directory `/data/db` which is set as default path.  

you can check this by running this command:

```bash
$ mongod dbpath
2020-03-30T00:57:56.044+0900 I  CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
/data/db
```

so what we can do is:

* create `~/data/db`
  
  ```bash
  mkdir -pv ~/data/db
  ```

* set `~/data/db` as data directory

  ```bash
  mongod --dbpath ~/data/db
  ```

now, run it again with `mongod --dbpath ~data/db

```bash
$ mongod --dbpath ~/data/db
2020-03-30T00:59:29.858+0900 I  CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2020-03-30T00:59:29.861+0900 I  CONTROL  [initandlisten] MongoDB starting : pid=61169 port=27017 dbpath=data/db 64-bit host=Juns-MacBook-Pro.local
2020-03-30T00:59:29.861+0900 I  CONTROL  [initandlisten] db version v4.2.3
2020-03-30T00:59:29.861+0900 I  CONTROL  [initandlisten] git version: 6874650b362138df74be53d366bbefc321ea32d4
2020-03-30T00:59:29.861+0900 I  CONTROL  [initandlisten] allocator: system
2020-03-30T00:59:29.861+0900 I  CONTROL  [initandlisten] modules: none
2020-03-30T00:59:29.861+0900 I  CONTROL  [initandlisten] build environment:
2020-03-30T00:59:29.861+0900 I  CONTROL  [initandlisten]     distarch: x86_64
2020-03-30T00:59:29.861+0900 I  CONTROL  [initandlisten]     target_arch: x86_64
2020-03-30T00:59:29.861+0900 I  CONTROL  [initandlisten] options: { storage: { dbPath: "data/db" } }
2020-03-30T00:59:29.862+0900 I  STORAGE  [initandlisten] wiredtiger_open config: create,cache_size=7680M,cache_overflow=(file_max=0M),session_max=33000,eviction=(threads_min=4,threads_max=4),config_base=false,statistics=(fast),log=(enabled=true,archive=true,path=journal,compressor=snappy),file_manager=(close_idle_time=100000,close_scan_interval=10,close_handle_minimum=250),statistics_log=(wait=0),verbose=[recovery_progress,checkpoint_progress],
2020-03-30T00:59:30.521+0900 I  STORAGE  [initandlisten] WiredTiger message [1585497570:521444][61169:0x1100f7dc0], txn-recover: Set global recovery timestamp: (0, 0)
2020-03-30T00:59:30.599+0900 I  RECOVERY [initandlisten] WiredTiger recoveryTimestamp. Ts: Timestamp(0, 0)
2020-03-30T00:59:30.660+0900 I  STORAGE  [initandlisten] Timestamp monitor starting
2020-03-30T00:59:30.662+0900 I  CONTROL  [initandlisten]
2020-03-30T00:59:30.662+0900 I  CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2020-03-30T00:59:30.662+0900 I  CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2020-03-30T00:59:30.662+0900 I  CONTROL  [initandlisten]
2020-03-30T00:59:30.662+0900 I  CONTROL  [initandlisten] ** WARNING: This server is bound to localhost.
2020-03-30T00:59:30.662+0900 I  CONTROL  [initandlisten] **          Remote systems will be unable to connect to this server.
2020-03-30T00:59:30.662+0900 I  CONTROL  [initandlisten] **          Start the server with --bind_ip <address> to specify which IP
2020-03-30T00:59:30.662+0900 I  CONTROL  [initandlisten] **          addresses it should serve responses from, or with --bind_ip_all to
2020-03-30T00:59:30.663+0900 I  CONTROL  [initandlisten] **          bind to all interfaces. If this behavior is desired, start the
2020-03-30T00:59:30.663+0900 I  CONTROL  [initandlisten] **          server with --bind_ip 127.0.0.1 to disable this warning.
2020-03-30T00:59:30.663+0900 I  CONTROL  [initandlisten]
2020-03-30T00:59:30.663+0900 I  CONTROL  [initandlisten]
2020-03-30T00:59:30.663+0900 I  CONTROL  [initandlisten] ** WARNING: soft rlimits too low. Number of files is 256, should be at least 1000
2020-03-30T00:59:30.664+0900 I  STORAGE  [initandlisten] createCollection: admin.system.version with provided UUID: 7070d56b-aff6-4ef9-8618-696ac37acce9 and options: { uuid: UUID("7070d56b-aff6-4ef9-8618-696ac37acce9") }
2020-03-30T00:59:30.714+0900 I  INDEX    [initandlisten] index build: done building index _id_ on ns admin.system.version
2020-03-30T00:59:30.715+0900 I  SHARDING [initandlisten] Marking collection admin.system.version as collection version: <unsharded>
2020-03-30T00:59:30.715+0900 I  COMMAND  [initandlisten] setting featureCompatibilityVersion to 4.2
2020-03-30T00:59:30.715+0900 I  SHARDING [initandlisten] Marking collection local.system.replset as collection version: <unsharded>
2020-03-30T00:59:30.716+0900 I  STORAGE  [initandlisten] Flow Control is enabled on this deployment.
2020-03-30T00:59:30.716+0900 I  SHARDING [initandlisten] Marking collection admin.system.roles as collection version: <unsharded>
2020-03-30T00:59:30.716+0900 I  STORAGE  [initandlisten] createCollection: local.startup_log with generated UUID: ad6e0525-79bb-42b8-8dde-1ef02ae82944 and options: { capped: true, size: 10485760 }
2020-03-30T00:59:30.762+0900 I  INDEX    [initandlisten] index build: done building index _id_ on ns local.startup_log
2020-03-30T00:59:30.762+0900 I  SHARDING [initandlisten] Marking collection local.startup_log as collection version: <unsharded>
2020-03-30T00:59:30.762+0900 I  FTDC     [initandlisten] Initializing full-time diagnostic data capture with directory 'data/db/diagnostic.data'
2020-03-30T00:59:30.764+0900 I  SHARDING [LogicalSessionCacheRefresh] Marking collection config.system.sessions as collection version: <unsharded>
2020-03-30T00:59:30.764+0900 I  NETWORK  [listener] Listening on /tmp/mongodb-27017.sock
2020-03-30T00:59:30.764+0900 I  NETWORK  [listener] Listening on 127.0.0.1
2020-03-30T00:59:30.764+0900 I  CONTROL  [LogicalSessionCacheReap] Sessions collection is not set up; waiting until next sessions reap interval: config.system.sessions does not exist
2020-03-30T00:59:30.764+0900 I  NETWORK  [listener] waiting for connections on port 27017
2020-03-30T00:59:30.764+0900 I  STORAGE  [LogicalSessionCacheRefresh] createCollection: config.system.sessions with provided UUID: e7546955-0fc0-4b38-9ebd-4a6d8be41db1 and options: { uuid: UUID("e7546955-0fc0-4b38-9ebd-4a6d8be41db1") }
2020-03-30T00:59:30.809+0900 I  INDEX    [LogicalSessionCacheRefresh] index build: done building index _id_ on ns config.system.sessions
2020-03-30T00:59:30.880+0900 I  INDEX    [LogicalSessionCacheRefresh] index build: starting on config.system.sessions properties: { v: 2, key: { lastUse: 1 }, name: "lsidTTLIndex", ns: "config.system.sessions", expireAfterSeconds: 1800 } using method: Hybrid
2020-03-30T00:59:30.880+0900 I  INDEX    [LogicalSessionCacheRefresh] build may temporarily use up to 200 megabytes of RAM
2020-03-30T00:59:30.880+0900 I  INDEX    [LogicalSessionCacheRefresh] index build: collection scan done. scanned 0 total records in 0 seconds
2020-03-30T00:59:30.881+0900 I  INDEX    [LogicalSessionCacheRefresh] index build: inserted 0 keys from external sorter into index in 0 seconds
2020-03-30T00:59:30.891+0900 I  INDEX    [LogicalSessionCacheRefresh] index build: done building index lsidTTLIndex on ns config.system.sessions
2020-03-30T00:59:30.902+0900 I  COMMAND  [LogicalSessionCacheRefresh] command config.system.sessions command: createIndexes { createIndexes: "system.sessions", indexes: [ { key: { lastUse: 1 }, name: "lsidTTLIndex", expireAfterSeconds: 1800 } ], $db: "config" } numYields:0 reslen:114 locks:{ ParallelBatchWriterMode: { acquireCount: { r: 2 } }, ReplicationStateTransition: { acquireCount: { w: 3 } }, Global: { acquireCount: { r: 1, w: 2 } }, Database: { acquireCount: { r: 1, w: 2, W: 1 } }, Collection: { acquireCount: { r: 4, w: 1, R: 1, W: 2 } }, Mutex: { acquireCount: { r: 3 } } } flowControl:{ acquireCount: 1 } storage:{} protocol:op_msg 138ms
2020-03-30T00:59:31.002+0900 I  SHARDING [ftdc] Marking collection local.oplog.rs as collection version: <unsharded>
```

Thus, we can successfully run the MongoDB.

---

## 52. Instal MongoDB - Windows Instruction

* Install MongoDB on Windows
  * If you're having issues, please look at these tutorials:
    * [instal mongodb on windows](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
    * [mongo-windows](https://treehouse.github.io/installation-guides/windows/mongo-windows.html)
  * If you want to use a custom data directory
    * Create C:/database_mongo
    * mongod --dbpath=C:/database_mongo/

---

## 53. Instal MongoDB UI - Robo 3T

* robomongo renamed as Robo 3T
  * download: [link](https://robomongo.org/download)

* after the app installed:
  * open the app
  * create connection with this spec:
    * Type: Direct Connection
    * Name: localhost
    * Address: localhost:27017
  * click the "test" button at bottom left
    * you will get this message:
      * Connected to **localhost:27017**
      * Access to databases is available
  * save this setting
  * and now you are ready to connect.

![robo3t](./robo-3t.png)

---

## 54. Blog Service Golang Setup

### 54.1. Project Structure

* create directory like this:

```note
blog
  blog_client
    client.go
  blog_server
    server.go
  blog_pb
    blog.proto

calculator
  ...

greet
  ...

ssl
  ...
---

with this:

```bash
mkdir -pv blog/blog_client blog/blog_server blog/blogpb
```

### 54.2. Protobuf Definition

at the `blog/blogpb/blog.proto`, let's define the protobuf like below

```proto
syntax = "proto3";

package blog;

option go_package = "blogpb";

message Blog {
  string id = 1;
  string author_id = 2;
  string title = 3;
  string content = 4;
}

service BlogService {
  
}
```

and generate the code:

```bash
protoc blog/blogpb/blog.proto --go_out=plugins=grpc:.
```

and we get `blog/blogpb/blog.pb.go` file.

### 54.3. Server

We have `blog/blog_server/server.go` and it's empty file now.
What we want to do is:

* this time, we want to properly close the server
* modify to our blog service

so, first the simple code of the `server.go` looks like this:

```go
package main

import (
  "fmt"
  "log"
  "net"

  "google.golang.org/grpc"

  "../blogpb"
)

type server struct{
}

func main() {
  fmt.Println("Blog Service Started")

  lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
  if err != nil {
    log.Fatalf("Failed to listen: %v", err)
  }

  opts := []grpc.ServerOption{}
  s := grpc.NewServer(opts...)
  blogpb.RegisterBlogServiceServer(s, &server{})

  if err := s.Serve(lis); err != nil {
    log.Fatalf("Failed to serve: %v", err)
  }
}
```

but, it's not really "graceful".

> "How to properly stop the server?"

setup the "shut-down hook" that is able to handle an interrupt signal.

```go
package main

import (
  "fmt"
  "log"
  "net"
  "os"
  "os/signal"

  "google.golang.org/grpc"

  "../blogpb"
)

type server struct{
}

func main() {
  fmt.Println("Blog Service Started")

  lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
  if err != nil {
    log.Fatalf("Failed to listen: %v", err)
  }

  opts := []grpc.ServerOption{}
  s := grpc.NewServer(opts...)
  blogpb.RegisterBlogServiceServer(s, &server{})

  go func() {
    fmt.Println("Starting Server...")
    if err := s.Serve(lis); err != nil {
      log.Fatalf("Failed to serve: %v", err)
    }
  }()

  // With for Control C to exit
  ch := make(chan os.Signal, 1)
  signal.Notify(ch, os.Interrupt) // os.Interrupt by Control + C

  // Block until a signal is received
  <-ch
  fmt.Println("Stopping the server")
  s.Stop()
  fmt.Println("Closing the listener")
  lis.Close()
  fmt.Println("End of Program")
}
```

so the code:

```go
  // With for Control C to exit
  ch := make(chan os.Signal, 1)
  signal.Notify(ch, os.Interrupt) // os.Interrupt by Control + C
```

can intercept the interrupt signal correctly. `os.Interrupt` is equivalent to `control + C`.

Run it and close the server with `Control + C`:

```bash
$ go run blog/blog_server/server.go
Blog Service Started
Starting Server...
^CStopping the server
Closing the listener
End of Program
```

In addition, we can improve the logging:

```go
// ...
func main() {
  // if we crash the go code, we get the file name and line number
  log.SetFlags(log.LstdFlags | log.Lshortfile)

  // ...
```

let's run the server:

```bash
$ go run blog/blog_server/server.go
Blog Service Started
Starting Server...
```

run it on another terminal (to get error due to gRPC port is occupied):

```bash
$ go run blog/blog_server/server.go
Blog Service Started
2020/04/06 02:01:51 server.go:25: Failed to listen: listen tcp 0.0.0.0:50051: bind: address already in use
exit status 1
```

From the other terminal, you can see that which line of code has issue: (`server.go:25`) which is:

```go
    log.Fatalf("Failed to listen: %v", err)
```

so we can easily catch where to debug!

---

## 55. MongoDB Driver Golang Setup

* next things we have to do:
  * to setup MongoDB drivers for Go program
  * Google `mongodb driver golang`
    * you will find: [mongo-go-driver](https://github.com/mongodb/mongo-go-driver)
      * there is [go-mgo](https://github.com/go-mgo/mgo) option, but we won't use it this time.

how to install:

```bash
go get go.mongodb.org/mongo-driver/mongo
```

NOTE:

* mongo-go-driver is quite hard to use
* might take some time to figure out how to use properly
* there are some examples:
  * [examples/documentation_examples](https://github.com/mongodb/mongo-go-driver/tree/master/examples/documentation_examples)
* have a look [godoc/mongo](https://godoc.org/go.mongodb.org/mongo-driver/mongo)

### 55.1. Mongo DB setup with the server.go

Basic usage of the driver starts with creating a Client from a connection string. To do so, call the `NewClient` and `Connect` functions:

We use insecure mode, so we don't need to put ID:password as "`mongodb:foo:bar@//localhost:27017`" but use this: "`mongodb://localhost:27017`"

```go
// connect to MongoDB
client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
if err != nil { log.Fatal(err) }
ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
defer cancel()
err = client.Connect(ctx)
if err != nil { log.Fatal(err) }
```

and then, to run the database, what we have to do is "open up a collection", so we'll use our collection which is basically "**our table**".

```go
collection := client.Database("mydb").Collection("blog")
```

If the database (e.g. `mydb`) is not existed, it will create one for us. We can read the Go code above as

> from the `client`, connect to the `Database` which is called `mydb`, collection-wise, use `blog` (collection basically means similar to a "table" of a relational database world))

and we want to make the `collection` globally accessible:

```go
// ...

var collection *mongo.Collection

func main() {
// ...
}
```

We'll use this code for the `blog/blog_server/server.go`

```go
package main

import (
  "context"
  "fmt"
  "go.mongodb.org/mongo-driver/mongo"
  "go.mongodb.org/mongo-driver/mongo/options"
  "log"
  "net"
  "os"
  "os/signal"
  "time"

  "google.golang.org/grpc"

  "../blogpb"
)

var collection *mongo.Collection

type server struct {
}

func main() {
  // if we crash the go code, we get the file name and line number
  log.SetFlags(log.LstdFlags | log.Lshortfile)

  fmt.Println("Blog Service Started")

  // connect to MongoDB
  client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
  if err != nil {
    log.Fatal(err)
  }
  ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
  defer cancel()
  err = client.Connect(ctx)
  if err != nil {
    log.Fatal(err)
  }

  collection = client.Database("mydb").Collection("blog")

  lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
  if err != nil {
    log.Fatalf("Failed to listen: %v", err)
  }

  opts := []grpc.ServerOption{}
  s := grpc.NewServer(opts...)
  blogpb.RegisterBlogServiceServer(s, &server{})

  go func() {
    fmt.Println("Starting Server...")
    if err := s.Serve(lis); err != nil {
      log.Fatalf("Failed to serve: %v", err)
    }
  }()

  // With for Control C to exit
  ch := make(chan os.Signal, 1)
  signal.Notify(ch, os.Interrupt) // os.Interrupt by Control + C

  // Block until a signal is received
  <-ch
  fmt.Println("Stopping the server")
  s.Stop()
  fmt.Println("Closing the listener")
  lis.Close()
  fmt.Println("End of Program")
}
```

* Other things we have to do:
  * creating a "data model" or "data definition"
    * to hold the data over `blog` into a `MongoDB`
    * need to define the types of each field and map them to [BSON](https://en.wikipedia.org/wiki/BSON)
      * e.g. `ID primitive.ObjectID`, this is MongoDB specific thing
      * `primitive.ObjectID` used to be `objectid.ObjectID`
    * also we need to add data we defined at protobuf

```go
type blogItem struct {
  ID       primitive.ObjectID
  AuthorID string
  Context  string
  Title    string
}
```

Then, we need to add "tags" to add `bson` information. For example:

```go
ID       primitive.ObjectID `bson:"_id,omitempty"`
```

means, the field `ID` is going to be mapped `bson` field, named `_id`, and it's not existed, we omitted it (since we are using `omitempty` option)

```go
type blogItem struct {
  ID       primitive.ObjectID `bson:"_id,omitempty"`
  AuthorID string             `bson:"author_id"`
  Context  string             `bson:"context"`
  Title    string             `bson:"title"`
}
```

Finally, when we stop the server, we also need to stop the connection to the MongoDB.

```go
  // ...
  lis.Close()
  // ...
  fmt.Println("Closing MongoDB Connection")
  client.Disconnect(context.TODO())
  fmt.Printlin("End of Program")
}
```

Minor update is add logging on the right place for better logging:

* `fmt.Println("Connecting to MongoDB")`
* `fmt.Println("Blog Service Started")`

The entire code looks like:

```go
package main

import (
  "context"
  "fmt"
  "go.mongodb.org/mongo-driver/bson/primitive"
  "go.mongodb.org/mongo-driver/mongo"
  "go.mongodb.org/mongo-driver/mongo/options"
  "log"
  "net"
  "os"
  "os/signal"
  "time"

  "google.golang.org/grpc"

  "../blogpb"
)

var collection *mongo.Collection

type server struct {
}

type blogItem struct {
  ID       primitive.ObjectID `bson:"_id,omitempty"`
  AuthorID string             `bson:"author_id"`
  Context  string             `bson:"context"`
  Title    string             `bson:"title"`
}

func main() {
  // if we crash the go code, we get the file name and line number
  log.SetFlags(log.LstdFlags | log.Lshortfile)

  fmt.Println("Connecting to MongoDB")
  // connect to MongoDB
  client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
  if err != nil {
    log.Fatal(err)
  }
  ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
  defer cancel()
  err = client.Connect(ctx)
  if err != nil {
    log.Fatal(err)
  }

  fmt.Println("Blog Service Started")
  collection = client.Database("mydb").Collection("blog")

  lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
  if err != nil {
    log.Fatalf("Failed to listen: %v", err)
  }

  opts := []grpc.ServerOption{}
  s := grpc.NewServer(opts...)
  blogpb.RegisterBlogServiceServer(s, &server{})

  go func() {
    fmt.Println("Starting Server...")
    if err := s.Serve(lis); err != nil {
      log.Fatalf("Failed to serve: %v", err)
    }
  }()

  // With for Control C to exit
  ch := make(chan os.Signal, 1)
  signal.Notify(ch, os.Interrupt) // os.Interrupt by Control + C

  // Block until a signal is received
  <-ch
  fmt.Println("Stopping the server")
  s.Stop()
  fmt.Println("Closing the listener")
  lis.Close()
  fmt.Println("Closing MongoDB Connection")
  client.Disconnect(context.TODO())
  fmt.Println("End of Program")
}
```

make sure all code works well:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
^CStopping the server
Closing the listener
Closing MongoDB Connection
End of Program
```

Thus, we can see:

* connect to the MongoDB, if success
* start the server
* got an interrupt signal, so stopping the server
* closing the listener
* closing the MongoDB connection
* program ended

---

## 56. Code Changes

* Important: Code Changes
* Some MongoDB methods (just a few)
* The changes are minor and summarized [here](https://github.com/simplesteph/grpc-go-course/pull/1/files)
* the latest working code: [here](https://github.com/simplesteph/grpc-go-course)

The changes are:

* `mongo-go-driver/bson/primitive` (used to be: `mongo-go-driver/bson/objectid"`)
* `primitive.ObjectID` (used to be: `objectid.ObjectID`)
* `primitive.ObjectIDFromHex(blogID)` (used to be: `objectid.FromHex(blogID)`)
* `bson.M{"_id": oid}` (used to be: `bson.NewDocument(bson.EC.ObjectID("_id", oid))`)

---

## 57. CreateBlog Server

### 57.1. Protobuf

```proto
syntax = "proto3";

package blog;

option go_package = "blogpb";

message Blog {
  string id = 1;
  string author_id = 2;
  string title = 3;
  string content = 4;
}

message CreateBlogRequest {
  Blog blog = 1;
}

message CreateBlogResponse {
  Blog blog = 1;  // will have a blog id
}

service BlogService {
  rpc CreateBlog (CreateBlogRequest) returns (CreateBlogResponse) {};
}
```

and generate our code:

```bash
protoc blog/blogpb/blog.proto --go_out=plugins=grpc:.
```

### 57.2. Server

* implement `CreateBlog()` at `blog/blog_server/server.go`
  * parse the contents of the request and pass it to our database, MongoDB

```go
func (*server) CreateBlog(ctx context.Context, req *blogpb.CreateBlogRequest) (*blogpb.CreateBlogResponse, error) {
  // ...
}
```

here is the result:

```go
func (*server) CreateBlog(ctx context.Context, req *blogpb.CreateBlogRequest) (*blogpb.CreateBlogResponse, error) {
  blog := req.GetBlog()

  data := blogItem{
    AuthorID: blog.GetAuthorId(),
    Context:  blog.GetContent(),
    Title:    blog.GetTitle(),
  }

  res, err := collection.InsertOne(context.Background(), data)
  if err != nil {
    return nil, status.Errorf(
      codes.Internal,
      fmt.Sprintf("Internal error: %v", err),
    )
  }
  oid, ok := res.InsertedID.(primitive.ObjectID) // oid means an object ID
  if !ok {
    return nil, status.Errorf(
      codes.Internal,
      fmt.Sprintf("Cannot convert to OID"),
    )
  }

  return &blogpb.CreateBlogResponse{
    Blog: &blogpb.Blog{
      Id:       oid.Hex(),
      AuthorId: blog.GetAuthorId(),
      Title:    blog.GetTitle(),
      Content:  blog.GetContent(),
    },
  }, nil
}
```

make sure the server can be run:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
```

---

## 58. CreateBlog Client

* this would be similar to Greet service, so we will take `greet/greet_client/client.go`

```go
package main

import (
  "context"
  "fmt"
  "google.golang.org/grpc"
  "log"

  "../blogpb"
)

func main() {
  fmt.Println("Blog Client")

  opts := grpc.WithInsecure()

  cc, err := grpc.Dial("localhost:50051", opts)
  if err != nil {
    log.Fatalf("could not connect: %v", err)
  }
  defer cc.Close()

  c := blogpb.NewBlogServiceClient(cc)

  // create Blog
  fmt.Println("Creating the blog")
  blog := &blogpb.Blog{
    AuthorId: "Mark",
    Title:    "My First Blog",
    Content:  "Content of the first blog",
  }
  createBlogRes, err := c.CreateBlog(context.Background(), &blogpb.CreateBlogRequest{Blog: blog})
  if err != nil {
    log.Fatalf("Unexpected err: %v", err)
  }
  fmt.Printf("Blog has been created: %v", createBlogRes)
}
```

in the previous part, we run the server, thus assume the server is running still:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
```

and in another terminal, run the client:

```bash
$ go run blog/blog_client/client.go
Blog Client
Creating the blog
Blog has been created: blog:<id:"5e932a6cb7b07da9e40057a7" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
```

but the server-side log does now show any, add more log on `blog/blog_server/server.go`. In this case, just for tracking purpose, we add simple print message at the beginning of the `func CreateBlog()`.

```go
// ...
func (*server) CreateBlog(ctx context.Context, req *blogpb.CreateBlogRequest) (*blogpb.CreateBlogResponse, error) {
  fmt.Println("Create blog request")
  // ...
```

after this, run the server again:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
```

and run the client

```bash
$ go run blog/blog_client/client.go
Blog Client
Creating the blog
Blog has been created: blog:<id:"5e932b620f97f9e193a3c5e8" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
```

the server shows this message also:

```bash
Create blog request
```

**NOTE**: Make sure that your MongoDB server is running in a separate terminal.

### 58.1. How to Make Sure Everything Runs Correctly

* Use Robo 3T
* refresh the app
  * there is `mydb` under `Localhost`
  * under `mydb` we've got `Collections`
  * under `Collections` we have `blog` and when you click it
  * and we can see some objects

![robo3t-with-data](./robo-3t-with-data.png)

---

## 59. ReadBlog Server

* add rpc for `ReadBlog`

### 59.1. Protobuf

```proto
// ...

message ReadBlogRequest {
  string blog_id = 1;
}

message ReadBlogResponse {
  Blog blog = 1;
}

service BlogService {
  rpc CreateBlog (CreateBlogRequest) returns (CreateBlogResponse);
  rpc ReadBlog (ReadBlogRequest) returns (ReadBlogResponse);  // return NOT_FOUND if not found
}
```

and generate the code:

```bash
protoc blog/blogpb/blog.proto --go_out=plugins=grpc:.
```

or

```bash
source generation.sh
```

now, it's ready to write the server code

### 59.2. Server

* implement `blog/blog_server/server.go` with the new RPC, `ReadBlog`

```go
func (*server) ReadBlog(ctx context.Context, req *blogpb.ReadBlogRequest) (*blogpb.ReadBlogResponse, error) {
  fmt.Println("Read blog request")
  blogID := req.GetBlogId()

  oid, err := primitive.ObjectIDFromHex(blogID)
  if err != nil {
    return nil, status.Errorf(
      codes.InvalidArgument,
      fmt.Sprintf("Cannot parse ID"),
    )
  }

  // create an empty struct
  data := &blogItem{}
  filter := bson.M{"_id": oid}

  res := collection.FindOne(context.Background(), filter)
  if err := res.Decode(data); err != nil {
    return nil, status.Errorf(
      codes.NotFound,
      fmt.Sprintf("Cannot find blog with specified ID: %v", err),
    )
  }

  return &blogpb.ReadBlogResponse{
    Blog: &blogpb.Blog{
      Id:       data.ID.Hex(),
      AuthorId: data.AuthorID,
      Title:    data.Title,
      Content:  data.Context,
    },
  }, nil
}
```

check the server is runnable or not:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
```

---

## 60. ReadBlog Client

on the previous client code, inside of the `main()` funciton we add this:

```go
func main() {
  // ...
  fmt.Printf("Blog has been created: %v\n", createBlogRes)
  blogID := createBlogRes.GetBlog().GetId()

  // read Blog
  fmt.Println("Reading the blog")

  _, err2 := c.ReadBlog(context.Background(), &blogpb.ReadBlogRequest{BlogId:"5e93411f11844eecb9e7787d"})
  if err2 != nil {
    fmt.Printf("Error happened whilst reading: %v\n", err2)
  }

  readBlogReq := &blogpb.ReadBlogRequest{BlogId: blogID}
  readBlogRes, readBlogErr := c.ReadBlog(context.Background(), readBlogReq)
  if readBlogErr != nil {
    fmt.Printf("Error happened whilst reading: %v\n", readBlogErr)
  }

  fmt.Printf("Blog was read: %v", readBlogRes)
}
```

and run the server:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
```

then run the client:

```bash
$ go run blog/blog_client/client.go
Blog Client
Creating the blog
Blog has been created: blog:<id:"5e93411f11844eecb9e7787c" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
Reading the blog
Error happened whilst reading: rpc error: code = InvalidArgument desc = Cannot parse ID
Blog was read: blog:<id:"5e93411f11844eecb9e7787c" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
```

you get this message from server-side as well:

```bash
Create blog request
Read blog request
Read blog request
```

---

## 61. UpdateBlog Server

In the previous part, we learnt how to do "read", so here, we are going to cover how to "update" the data.

### 61.1. Protobuf

```proto
message UpdateBlogRequest {
  Blog blog = 1;
}

message UpdateBlogResponse {
  Blog blog = 1;
}

service BlogService {
  rpc CreateBlog (CreateBlogRequest) returns (CreateBlogResponse);
  rpc ReadBlog (ReadBlogRequest) returns (ReadBlogResponse);  // return NOT_FOUND if not found
  rpc UpdateBlog (UpdateBlogRequest) returns (UpdateBlogResponse);  // return NOT_FOUND if not found
}
```

and generate the code:

```bash
protoc blog/blogpb/blog.proto --go_out=plugins=grpc:.
```

### 61.2. Server

```go

func dataToBlogPb(data *blogItem) *blogpb.Blog {
  return &blogpb.Blog{
    Id:       data.ID.Hex(),
    AuthorId: data.AuthorID,
    Title:    data.Title,
    Content:  data.Context,
  }
}

func (*server) UpdateBlog(ctx context.Context, req *blogpb.UpdateBlogRequest) (*blogpb.UpdateBlogResponse, error) {
  fmt.Println("Update blog request")
  blog := req.GetBlog()
  oid, err := primitive.ObjectIDFromHex(blog.GetId())
  if err != nil {
    return nil, status.Errorf(
      codes.InvalidArgument,
      fmt.Sprintf("Cannot parse ID"),
    )
  }

  // create an empty struct
  data := &blogItem{}
  filter := bson.M{"_id": oid}

  res := collection.FindOne(context.Background(), filter)
  if err := res.Decode(data); err != nil {
    return nil, status.Errorf(
      codes.NotFound,
      fmt.Sprintf("Cannot find blog with specified ID: %v", err),
    )
  }

  // we update our internal struct
  data.AuthorID = blog.GetAuthorId()
  data.Context = blog.GetContent()
  data.Title = blog.GetTitle()

  _, updateErr := collection.ReplaceOne(context.Background(), filter, data)
  if updateErr != nil {
    return nil, status.Errorf(
      codes.Internal,
      fmt.Sprintf("Cannot update object in MongoDB: %v", updateErr),
    )
  }

  return &blogpb.UpdateBlogResponse{
    Blog: dataToBlogPb(data),
  }, nil
}
```

NOTE: obviously we can use `collection.ReplaceOne` without using `collection.FindOne` to reduce 2 database calls to 1 database call.

---

## 62. UpdateBlog Client

We can simply add this code at the end of `func main()` of the client code:

```go
// ...

func main() {
  // ...

  // update Blog
  newBlog := &blogpb.Blog{
    Id:       blogID,
    AuthorId: "Changed Author",
    Title:    "My First Blog (edited)",
    Content:  "Content of the first blog, with some awesome additions!",
  }

  updateRes, updateErr := c.UpdateBlog(context.Background(), &blogpb.UpdateBlogRequest{Blog: newBlog})
  if updateErr != nil {
    fmt.Printf("Error happened whilst updating: %v\n", updateErr)
  }
  fmt.Printf("Blog was read: %v\n", updateRes)
}
```

run the server:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
```

run the client:

```bash
$ go run blog/blog_client/client.go
Blog Client
Creating the blog
Blog has been created: blog:<id:"5e9353c8a06e99328c8db55d" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
Reading the blog
Error happened whilst reading: rpc error: code = NotFound desc = Cannot find blog with specified ID: mongo: no documents in result
Blog was read: blog:<id:"5e9353c8a06e99328c8db55d" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
Blog was read: blog:<id:"5e9353c8a06e99328c8db55d" author_id:"Changed Author" title:"My First Blog (edited)" content:"Content of the first blog, with some awesome additions!" >
```

and server get:

```bash
Create blog request
Read blog request
Read blog request
Update blog request
```

thus, we can see it updates the data.

We can also see the updates from Robo 3T

![robo3t-with-update](robo-3t-with-update.png)

---

## 63. DeleteBlog Server

### 63.1. Protobuf

```proto
message DeleteBlogRequest {
  string blog_id = 1;
}

message DeleteBlogResponse {
  string blog_id = 1;
}

service BlogService {
  rpc CreateBlog (CreateBlogRequest) returns (CreateBlogResponse);
  rpc ReadBlog (ReadBlogRequest) returns (ReadBlogResponse);  // return NOT_FOUND if not found
  rpc UpdateBlog (UpdateBlogRequest) returns (UpdateBlogResponse);  // return NOT_FOUND if not found
  rpc DeleteBlog (DeleteBlogRequest) returns (DeleteBlogResponse);  // return NOT_FOUND if not found
}
```

generate the code:

```bash
protoc blog/blogpb/blog.proto --go_out=plugins=grpc:.
```

### 63.2. Server

```go
func (*server) DeleteBlog(ctx context.Context, req *blogpb.DeleteBlogRequest) (*blogpb.DeleteBlogResponse, error) {
  fmt.Println("Delete blog request")
  oid, err := primitive.ObjectIDFromHex(req.GetBlogId())
  if err != nil {
    return nil, status.Errorf(
      codes.InvalidArgument,
      fmt.Sprintf("Cannot parse ID"),
    )
  }

  filter := bson.M{"_id": oid}

  res, err := collection.DeleteOne(context.Background(), filter)
  if err != nil {
    return nil, status.Errorf(
      codes.Internal,
      fmt.Sprintf("Cannot delete object in MongoDB: %v", err),
    )
  }

  if res.DeletedCount == 0 {
    return nil, status.Errorf(
      codes.NotFound,
      fmt.Sprintf("Cannot find blog in MongoDB: %v", err),
    )
  }

  return &blogpb.DeleteBlogResponse{
    BlogId: req.GetBlogId(),
  }, nil
}
```

---

## 64. DeleteBlog Client

add this code at the end of the current `func main()` of the client code:

```go
// ...
func main() {
  // ...

  // delete Blog
  deleteRes, deleteErr := c.DeleteBlog(context.Background(), &blogpb.DeleteBlogRequest{BlogId:blogID})
  if deleteErr != nil {
    fmt.Printf("Error happened whlist deleting: %v\n" deleteErr)
  }

  fmt.Printf("Blog was deleted: %v\n", deleteRes)
}
```

run the server:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
```

run the client:

```bash
$ go run blog/blog_client/client.go
Blog Client
Creating the blog
Blog has been created: blog:<id:"5e93585866f668aa7d1e4466" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
Reading the blog
Error happened whilst reading: rpc error: code = NotFound desc = Cannot find blog with specified ID: mongo: no documents in result
Blog was read: blog:<id:"5e93585866f668aa7d1e4466" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
Blog was read: blog:<id:"5e93585866f668aa7d1e4466" author_id:"Changed Author" title:"My First Blog (edited)" content:"Content of the first blog, with some awesome additions!" >
Blog was deleted: blog_id:"5e93585866f668aa7d1e4466"
```

server also gets:

```bash
Create blog request
Read blog request
Read blog request
Update blog request
Delete blog request
```

* Thus we can see:
  * (C)reate
  * (R)ead
  * (U)pdate
  * (D)elete

---

## 65. ListBlog Server

### 65.1. Protobuf

```proto
message ListBlogRequest {

}

message ListBlogResponse {
  Blog blog = 1;
}


service BlogService {
  rpc CreateBlog (CreateBlogRequest) returns (CreateBlogResponse);
  rpc ReadBlog (ReadBlogRequest) returns (ReadBlogResponse);  // return NOT_FOUND if not found
  rpc UpdateBlog (UpdateBlogRequest) returns (UpdateBlogResponse);  // return NOT_FOUND if not found
  rpc DeleteBlog (DeleteBlogRequest) returns (DeleteBlogResponse);  // return NOT_FOUND if not found
  rpc ListBlog (ListBlogRequest) returns (stream ListBlogResponse);
}
```

generate the code:

```bash
protoc blog/blogpb/blog.proto --go_out=plugins=grpc:.
```

### 65.2. Server

```go
func (*server) ListBlog(req *blogpb.ListBlogRequest, stream blogpb.BlogService_ListBlogServer) error {
  fmt.Println("List blog request")
  cur, err := collection.Find(context.Background(), bson.D{{}}) // since filter is empty, it will find every single blog in the database
  if err != nil {
    return status.Errorf(
      codes.Internal,
      fmt.Sprintf("Unknown internal error: %v", err),
    )
  }
  defer cur.Close(context.Background()) // when this function exits, cur will be closed
  // iterate over the cursor
  for cur.Next(context.Background()) {
    data := &blogItem{}
    err := cur.Decode(data)
    if err != nil {
      return status.Errorf(
        codes.Internal,
        fmt.Sprintf("Error whilst decoding data from MongoDB: %v", err),
      )
    }
    stream.Send(&blogpb.ListBlogResponse{Blog: dataToBlogPb(data)})
  }
  if err := cur.Err(); err != nil {
    return status.Errorf(
      codes.Internal,
      fmt.Sprintf("Unknown internal error: %v", err),
    )
  }
  return nil
}
```

* can see the usage of `cursor`
* how to interate amongst the `cursor` by using `cursor.Next()` function
* using the stream to send data via `stream.Send()`
  * a good usecase that streaming can be helpful when you have you have a database for backend

see this can be run:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
```

---

## 66. ListBlog Client

```go
// ...

func main() {
  // ...

  // list Blogs
  stream, err := c.ListBlog(context.Background(), &blogpb.ListBlogRequest{})
  if err != nil {
    log.Fatalf("error whilst calling ListBlog RPC: %v", err)
  }
  for {
    res, err := stream.Recv()
    if err != io.EOF {
      break
    }
    if err != nil {
      log.Fatalf("Something happened: %v", err)
    }
    fmt.Println(res.GetBlog())
  }
}
```

server is running, thus, run the client:

```bash
$ go run blog/blog_client/client.go
Blog Client
Creating the blog
Blog has been created: blog:<id:"5e93604e82d461ebf63d66d2" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
Reading the blog
Error happened whilst reading: rpc error: code = NotFound desc = Cannot find blog with specified ID: mongo: no documents in result
Blog was read: blog:<id:"5e93604e82d461ebf63d66d2" author_id:"Mark" title:"My First Blog" content:"Content of the first blog" >
Blog was read: blog:<id:"5e93604e82d461ebf63d66d2" author_id:"Changed Author" title:"My First Blog (edited)" content:"Content of the first blog, with some awesome additions!" >
Blog was deleted: blog_id:"5e93604e82d461ebf63d66d2"
id:"5e932a6cb7b07da9e40057a7" author_id:"Mark" title:"My First Blog" content:"Content of the first blog"
id:"5e932ab6b7b07da9e40057a8" author_id:"Mark" title:"My First Blog" content:"Content of the first blog"
id:"5e932b620f97f9e193a3c5e8" author_id:"Mark" title:"My First Blog" content:"Content of the first blog"
id:"5e933f896d0f1f057f79c130" author_id:"Mark" title:"My First Blog" content:"Content of the first blog"
id:"5e9340196f97db4224a6c358" author_id:"Mark" title:"My First Blog" content:"Content of the first blog"
id:"5e93408611844eecb9e7787a" author_id:"Mark" title:"My First Blog" content:"Content of the first blog"
id:"5e9340a011844eecb9e7787b" author_id:"Mark" title:"My First Blog" content:"Content of the first blog"
id:"5e93411f11844eecb9e7787c" author_id:"Mark" title:"My First Blog" content:"Content of the first blog"
id:"5e93415b11844eecb9e7787d" author_id:"Mark" title:"My First Blog" content:"Content of the first blog"
id:"5e9353c8a06e99328c8db55d" author_id:"Changed Author" title:"My First Blog (edited)" content:"Content of the first blog, with some awesome additions!"
```

and server gets:

```bash
Create blog request
Read blog request
Read blog request
Update blog request
Delete blog request
List blog request
```

---

## 67. Evans CLI test with CRUD

* simply implement the reflection by adding this code:

```go
// Register reflection service on gRPC server.
reflection.Register(s)
```

to `func main()` so it should looks like:

```go
// ...

func main() {
  // ...

  opts := []grpc.ServerOption{}
  s := grpc.NewServer(opts...)
  blogpb.RegisterBlogServiceServer(s, &server{})

  // Register reflection service on gRPC server.
  reflection.Register(s)
  
  // ...
}
```

Now, the reflection is enabled!

Let's restart our server:

```bash
$ go run blog/blog_server/server.go
Connecting to MongoDB
Blog Service Started
Starting Server...
```

and use Evans:

```bash
$ evans -p 50051 -r

  ______
 |  ____|
 | |__    __   __   __ _   _ __    ___
 |  __|   \ \ / /  / _. | | '_ \  / __|
 | |____   \ V /  | (_| | | | | | \__ \
 |______|   \_/    \__,_| |_| |_| |___/

 more expressive universal gRPC client


blog.BlogService@127.0.0.1:50051>
```

now we've got into the interactive mode:

```bash
blog.BlogService@127.0.0.1:50051> show service
+-------------+------------+-------------------+--------------------+
|   SERVICE   |    RPC     |   REQUEST TYPE    |   RESPONSE TYPE    |
+-------------+------------+-------------------+--------------------+
| BlogService | CreateBlog | CreateBlogRequest | CreateBlogResponse |
| BlogService | ReadBlog   | ReadBlogRequest   | ReadBlogResponse   |
| BlogService | UpdateBlog | UpdateBlogRequest | UpdateBlogResponse |
| BlogService | DeleteBlog | DeleteBlogRequest | DeleteBlogResponse |
| BlogService | ListBlog   | ListBlogRequest   | ListBlogResponse   |
+-------------+------------+-------------------+--------------------+
```

select the blog service:

```bash
blog.BlogService@127.0.0.1:50051> service BlogService
```

calling CreateBlog:

```bash
blog.BlogService@127.0.0.1:50051> call CreateBlog
blog::id (TYPE_STRING) =>
blog::author_id (TYPE_STRING) => "Mark"
blog::title (TYPE_STRING) => "Blog with spaces, cool title"
blog::content (TYPE_STRING) => "This is a blog that was created using the CLI"
{
  "blog": {
    "id": "5e946523f1041074206ebd6b",
    "authorId": "\"Mark\"",
    "title": "\"Blog with spaces, cool title\"",
    "content": "\"This is a blog that was created using the CLI\""
  }
}
```

call ListBlog:

```bash
blog.BlogService@127.0.0.1:50051> call ListBlog
{
  "blog": {
    "id": "5e932a6cb7b07da9e40057a7",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e932ab6b7b07da9e40057a8",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e932b620f97f9e193a3c5e8",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e933f896d0f1f057f79c130",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e9340196f97db4224a6c358",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e93408611844eecb9e7787a",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e9340a011844eecb9e7787b",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e93411f11844eecb9e7787c",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e93415b11844eecb9e7787d",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e9353c8a06e99328c8db55d",
    "authorId": "Changed Author",
    "title": "My First Blog (edited)",
    "content": "Content of the first blog, with some awesome additions!"
  }
}
{
  "blog": {
    "id": "5e946523f1041074206ebd6b",
    "authorId": "\"Mark\"",
    "title": "\"Blog with spaces, cool title\"",
    "content": "\"This is a blog that was created using the CLI\""
  }
}
```

try to delete id with `5e93415b11844eecb9e7787d`:

```bash
blog.BlogService@127.0.0.1:50051> call DeleteBlog
blog_id (TYPE_STRING) => 5e93415b11844eecb9e7787d
{
  "blogId": "5e93415b11844eecb9e7787d"
}
```

check the id is actually deleted:

```bash

blog.BlogService@127.0.0.1:50051> call DeleteBlog
blog_id (TYPE_STRING) => 5e93415b11844eecb9e7787d
command call: failed to send a request: rpc error: code = NotFound desc = Cannot find blog in MongoDB: <nil>
```

call ListBlog again:

```bash
blog.BlogService@127.0.0.1:50051> call ListBlog
{
  "blog": {
    "id": "5e932a6cb7b07da9e40057a7",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e932ab6b7b07da9e40057a8",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e932b620f97f9e193a3c5e8",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e933f896d0f1f057f79c130",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e9340196f97db4224a6c358",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e93408611844eecb9e7787a",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e9340a011844eecb9e7787b",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e93411f11844eecb9e7787c",
    "authorId": "Mark",
    "title": "My First Blog",
    "content": "Content of the first blog"
  }
}
{
  "blog": {
    "id": "5e9353c8a06e99328c8db55d",
    "authorId": "Changed Author",
    "title": "My First Blog (edited)",
    "content": "Content of the first blog, with some awesome additions!"
  }
}
{
  "blog": {
    "id": "5e946523f1041074206ebd6b",
    "authorId": "\"Mark\"",
    "title": "\"Blog with spaces, cool title\"",
    "content": "\"This is a blog that was created using the CLI\""
  }
}
```

and read `5e9353c8a06e99328c8db55d`:

```bash
blog.BlogService@127.0.0.1:50051> call ReadBlog
blog_id (TYPE_STRING) => 5e9353c8a06e99328c8db55d
{
  "blog": {
    "id": "5e9353c8a06e99328c8db55d",
    "authorId": "Changed Author",
    "title": "My First Blog (edited)",
    "content": "Content of the first blog, with some awesome additions!"
  }
}
```

we can also update the data:

```bash

blog.BlogService@127.0.0.1:50051> call UpdateBlog
blog::id (TYPE_STRING) => 5e9353c8a06e99328c8db55d
blog::author_id (TYPE_STRING) => Changed Author
blog::title (TYPE_STRING) => Changed Title
blog::content (TYPE_STRING) => Changed Content
{
  "blog": {
    "id": "5e9353c8a06e99328c8db55d",
    "authorId": "Changed Author",
    "title": "Changed Title",
    "content": "Changed Content"
  }
```

and check the update has applied or not by using `ReadBlog` RPC:

```bash
blog.BlogService@127.0.0.1:50051> call ReadBlog
blog_id (TYPE_STRING) => 5e9353c8a06e99328c8db55d
{
  "blog": {
    "id": "5e9353c8a06e99328c8db55d",
    "authorId": "Changed Author",
    "title": "Changed Title",
    "content": "Changed Content"
  }
}
```

---
