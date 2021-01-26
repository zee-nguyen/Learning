# Session 09: [Hands-On] gRPC Advanced Feature Deep Dive

---

## 43. [Theory] Errors in gRPC

### 43.1. Error Codes

#### 43.1.1. Conventional HTTP Errors

* It is common for your API to something return error codes
* in HTTP, there are **many** error codes
  * 2xx for success
  * 3xx for ...
  * 4xx for ...
  * 5xx for ...
* Whilst HTTP codes are standardisied, they are not usually clear enough

#### 43.1.2. gRPC Errors

* with gRPC, there are a few error codes:
  * https://grpc.io/docs/guides/error.html
* there is also complete reference to implementation of error codes that close a lot of gaps with the documentation:
  * http://avi.im/grpc-errors
* if an application needs to return extra information on the top of an error code, it can use the metadata context

**General Errors:**

| **Case** | **Status Code** |
| --- | --- |
| Client application cancelled the request | `GRPC_STATUS_CANCELLED` |
| Deadline expired before server returned status | `GRPC_STATUS_DEADLINE_EXCEEDED` |
| Method not found on server | `GRPC_STATUS_UNIMPLEMENTED` |
| Server shutting down | `GRPC_STATUS_UNAVAILABLE` |
| Server threw an exception (or did something other than returning a status code to terminate the RPC) | `GRPC_STATUS_UNKNOWN` |

**Network Failures:**

| **Case** | **Status Code** |
| --- | --- |
| No data transmitted before deadline expires. Also applies to cases where some data is transmitted and no other failures are detected before the deadline expires | `GRPC_STATUS_DEADLINE_EXCEEDED`
| Some data transmitted (for example, the request metadata has been written to the TCP connection) before the connection breaks | `GRPC_STATUS_UNAVAILABLE`

**Protocol Errors:**

| **Case** | **Status Code** |
| --- | --- |
| Could not decompress but compression algorithm supported | `GRPC_STATUS_INTERNAL`
| Compression mechanism used by client not supported by the server | `GRPC_STATUS_UNIMPLEMENTED`
| Flow-control resource limits reached | `GRPC_STATUS_RESOURCE_EXHAUSTED`
| Flow-control protocol violation | `GRPC_STATUS_INTERNAL`
| Error parsing returned status | `GRPC_STATUS_UNKNOWN`
| Unauthenticated: credentials failed to get metadata | `GRPC_STATUS_UNAUTHENTICATED`
| Invalid host set in authority metadata | `GRPC_STATUS_UNAUTHENTICATED`
| Error parsing response protocol buffer | `GRPC_STATUS_INTERNAL`
| Error parsing request protocol buffer | `GRPC_STATUS_INTERNAL`

---

## 44. [Hands-On] Errors implementation

### 44.1. Error Codes: Hands-On

* let's implement an error message for a new `SquareRoot` Unary API
* we'll create `SquareRoot` RPC
* we'll implement `Server` with the error handling
* we'll implement `Client` with the error handling

### 44.2. the Implementation

#### 44.2.1. Protobuf

* define the `SquareRoot` RPC first, with unary req and resp):

```proto
...

message SquareRootRequest {
  int32 number = 1;
}

message SquareRootResponse {
  double number_root = 1;
}

service CalculatorService {
  ... // previous RPC definitions

  rpc SquareRoot(SquareRootRequest) returns (SquareRootResponse){};
}
```

* generate `caculator.pb` by using:

```bash
protoc calculator/calculatorpb/calculator.proto --go_out=plugins=grpc:.
```

* One of important things we should do: "documentation for error handling"
  * `// make a comment about error handling for each rpc`

```proto
...
service CalculatorService {
  ... // previous RPC definitions

  // error handling
  // this RPC will throw an exception if the sent number is negative
  // the error being sent is of type `INVALID_ARGUMENT`
  rpc SquareRoot(SquareRootRequest) returns (SquareRootResponse){};
}
```

#### 44.2.2. Server

now, we can go to the `calculator_server/server.go` and have to implement `SquareRoot`

```go
...

func (*server) SquareRoot(ctx context.Context, req *calculatorpb.SquareRootRequest) (*calculatorpb.SquareRootResponse, error) {
  fmt.Println("Received SquareRoot RPC")
  number := req.GetNumber()
  if number < 0 {
    return nil, status.Errorf(
      codes.InvalidArgument,
      fmt.Sprintf("Received a negative number: %v", number),
    )
  }
  return &calculatorpb.SquareRootResponse{
    NumberRoot: math.Sqrt(float64(number)),
  }, nil
}

...
```

#### 44.2.3. Client

The server is now supporting the `SquareRoot`, we need to update the client, `calculator_client/client.go`

```go
...

func main() {
  fmt.Println("Calculator Client")
  cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
  if err != nil {
    log.Fatalf("could not connect: %v", err)
  }
  defer cc.Close()

  c := calculatorpb.NewCalculatorServiceClient(cc)

  ...

  doErrUnary(c)
}

...

func doErrUnary(c calculatorpb.CalculatorServiceClient) {
  fmt.Println("Starting to do a SquareRoot Unary RPC...")

  // correct call
  doErrorCall(c, 10)

  // error call
  doErrorCall(c, -2)
}

func doErrorCall(c calculatorpb.CalculatorServiceClient, n int32) {
  resp, err := c.SquareRoot(context.Background(), &calculatorpb.SquareRootRequest{Number: n})
  if err != nil {
    // err converted into the respErr
    // which is gRPC-friendly error that has message and code
    // but only if this `err` is actual gRPC error
    // if NOT, you'll get `ok` being false,
    // you can throw the normal error (the else clause)
    respErr, ok := status.FromError(err)
    if ok {
      // actual error from gRPC (user error)
      fmt.Printf("Error message from server: %v\n", respErr.Message())
      fmt.Println(respErr.Code())
      if respErr.Code() == codes.InvalidArgument {
        fmt.Println("We probably sent a negative number!")
        return
      }
    } else {
      // bigger error, framework type of error
      log.Fatalf("Big Error calling SquareRoot: %v", err)
      return
    }
  }
  fmt.Printf("Result of square root of %v: %v\n", n, resp.GetNumberRoot())
}

...
```

* for the `codes.*` of `codes. we can also use another errors:
  * `codes.NotFound`
  * `codes.OutOfRange`
  * `codes.PermissionDenied`
  * and more ...

#### 44.2.4. Run Server and Client

Now, the server and client are written. Let's run the server:

```bash
go run calculator/calculator_server/server.go
```

and you will see this message:

```bash
Calculator Server
```

then, let's run the client:

```bash
go run calculator/calculator_client/client.go
```

by running the client, the client can send requests to the server so the server-side get this messages:

```bash
Received SquareRoot RPC
Received SquareRoot RPC
```

because client send request 2 times: one is valid request, the other is invalid request

and the client-side get the responses:

```bash
Calculator Client
Starting to do a SquareRoot Unary RPC...
Result of square root of 10: 3.1622776601683795
Error message from server: Received a negative number: -2
InvalidArgument
We probably sent a negative number!
```

---

## 45. [Theory] Deadlines

### 45.1. gRPC Deadlines

* Deadlines allow gRPC clients to specify how long they are willing to wait for an RPC to complete before the RPC is terminated with the error `DEADLINE_EXCEEDED`
* **The gRPC documentation recommends you set a deadline for ALL client RPC calls**
* Setting the deadline is up to you: how long do you feel your API should have to complete?
  * usually small APIs: 100 ms, 500 ms, or 1000 ms (if slower response is okay)
  * for long API call: 5 min?
  * but, it's up to you
* The server should check if the deadline has exceeded and cancel the work it is doing
* This blog describes deadline in depth: `https://grpc.io/blog/deadlines`
* **NOTE**: Deadlines are propagated across if gRPC alls are chained
  * A => B => C (deadline for A is passed to B and then passed to C)
  * thus, C would be "aware" of the deadline of the client A

---

## 46. [Hands-On] Deadlines

### 46.1. gRPC Deadlines: Hands On

* We'll implement the server to return the response after 3000 ms
* The server will check if the client has cancelled the request
* We'll implement the client to set a deadline of 5000 ms
* We'll implement the client to set a deadline of 1000 ms

### 46.2. the Implementation

#### 46.2.1. Protobuf

one more API implementation under `greet.proto`:

```proto
...

message GreetWithDeadlineRequest {
  Greeting greeting = 1;
}

message GreetWithDeadlineResponse {
  string result = 1;
}

service GreetService {
  ...

  // Unary With Deadline
  rpc GreetWithDeadline(GreetWithDeadlineRequest) returns (GreetWithDeadlineResponse) {};
}
```

generate the code:

```bash
protoc greet/greetpb/greet.proto --go_out=plugins=grpc:.
```

#### 46.2.2. Client

let's go to `greet/greet_client/client.go` and add implementation:

* add `doUnaryWithDeadline()` at the `main` func

```go
func main() {
  fmt.Println("Hello, I am a client.")

  cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure()) // WithInsecure() for just now testing
  if err != nil {
  log.Fatalf("Could not connect: %v", err)
  }

  defer cc.Close()

  c := greetpb.NewGreetServiceClient(cc)

  doUnaryWithDeadline(c, 5*time.Second) // should complete
  doUnaryWithDeadline(c, 1*time.Second) // should timeout
}
```

#### 46.2.3. Server

```go
...

func (*server) GreetWithDeadline(ctx context.Context, req *greetpb.GreetWithDeadlineRequest) (*greetpb.GreetWithDeadlineResponse, error) {
  fmt.Printf("GreetWithDeadline function was invoked with %v\n", req)
  for i := 0; i < 3; i++ {
    if ctx.Err() == context.Canceled {
      // the client canceled the request
      fmt.Println("The client canceled the request!")
      return nil, status.Error(codes.Canceled, "the client canceled the request!")
    }
    time.Sleep(1 * time.Second)
  }
  firstName := req.GetGreeting().GetFirstName()
  result := "Hello " + firstName
  res := &greetpb.GreetWithDeadlineResponse{
    Result: result,
  }
  return res, nil
}

...
```

#### 46.2.4. Run the Codes

run the server:

```bash
go run greet/greet_server/server.go
```

and your _server terminal_ shows:

```bash
Hello world!
```

and open another terminal and run the client:

```bash
go run greet/greet_client/client.go
```

your _server terminal_ outputs:

```bash
GreetWithDeadline function was invoked with greeting:<first_name:"Mark" last_name:"Hahn" >
GreetWithDeadline function was invoked with greeting:<first_name:"Mark" last_name:"Hahn" >
```

and your _client terminal_ returns:

```bash
Hello, I am a client.
Starting to do a UnaryWithDeadline RPC...
2020/03/19 02:15:19 Response from GreetWithDeadline: Hello Mark
Starting to do a UnaryWithDeadline RPC...
Timeout was hit! Deadline was exceeded
```

---

## 47. [Theory] SSL Security

* Transport Layer Security (TLS), and its now-deprecated predecessor, Secure Sockets Layer (SSL), are cryptographic protocols designed to provide communications security over a computer network.
  * details: [wikipedia](https://en.wikipedia.org/wiki/Transport_Layer_Security)

* SSL Encryption in gRPC
  * In production gRPC call should be running with encryption enabled
  * This is done by generating SSL certificates
  * SSL allows communication to be secure end-to-end and ensuring no man in the middle attack can be performed

How SSL works?

* The need for SSL Encryption (1/3)
  * when you communicate over the internet,
    * your data is visible by all servers that transfer your packet
  * any router in the middle can view the packets you're sending using **PLAIN TEXT**
  * **It is not secure enough when the data is sensitive

```note
       -----                              ----------------                          ---------
HTTP  | You | -------------------------- | U: admin       | ---------------------- | Website |
      |     |                            | P: supersecret |                        |         |
       -----                              ----------------                          ---------

       -----       ----------------       ------------       ----------------       ---------
HTTP  | You | --- | U: admin       | --- |   Router   | --- | U: admin       | --- | Website |
      |     |     | P: supersecret |     | (Internet) |     | P: supersecret |     |         |
       -----       ----------------       ------------       ----------------       ---------
```

* The need for SSL Encryption (2/3)
  * SSL allows clients and servers to encrypt packet

```note
       -------------                      ----------------                          ---------
SSL   | gRPC Client | ------------------ | eBCskdsjEQdkfj | ---------------------- | Website |
      |             |                    | VfEGezKehbB... |                        |         |
       -------------                      ----------------                          ---------

       ----------------                                                      ----------------  
      | U: admin       |                                                    | eBCskdsjEQdkfj |
      | P: supersecret | --- SSL Encryption --        -- SSL Decryption --- | VfEGezKehbB... |
       ----------------                      |        |                      ----------------
                                             |        |
       ----------------                      |        |                      ----------------
      | eBCskdsjEQdkfj | <--------------------        --------------------> | U: admin       |
      | VfEGezKehbB... |                                                    | P: supersecret |
       ----------------                                                      ----------------

```

* The need for SSL Encryption (2/3)
  * SSL enables clients and servers to securely exchanges data
  * Routers cannot view the content of the Internet packets
  * let's do a deep dive into how SSL works

```note
       --------       ----------------       ------------       ----------------       ---------
SSL   | gRPC   | --- | eBCskdsjEQdkfj | --- |   Router   | --- | eBCskdsjEQdkfj | --- | Website |
      | Client |     | VfEGezKehbB... |     | (Internet) |     | VfEGezKehbB... |     |         |
       --------      ----------------        ------------       ----------------       ---------
```

* What is SSL?
  * TLS (Transport Layer Security), successor of SSL, encrypts the connection between 2 endpoints for secure data exchange

    ```note
     ----------                                                                              ------------------------
    | computer | -----> SSL Protocol (https)/Secure and secret exchange of information ---> | https://www.google.com |
     ----------                                                                              ------------------------
    ```

  * based on SSL certificates (e.g. on the web browser, you may see: `Secure | https://www.google.com`)
  * two ways of using SSL (gRPC can use both):
    * 1-way verification, e.g. browser => WebServer (**ENCRYPTION**)
    * 2-way verification, e.g. SSL authentication (**AUTHENTICATION**)

* Detailed Setup of SSL for Encryption

```note
                                                                                                               -------------
                                                                                                              | Server PEM  |
                                                                                                              | Private Key |
                                                                                                               -------------
               ---
              |     -------------                          -------------    Send Signed Certificate             ------------
Certification |    |   CA Root   |   Trust Certificate    | Certificate | -----------------------------------> | Server CRT |
    Setup     |    |   Public    | ---------------------> |  Authority  |                                      | Signed by  |
              |    | Certificate |                        |    (CA)     | <----------------------------------- | CA         |
              |     -------------                          -------------       Request to sign server.crt       ------------
               ---        |                                                  certificate for myapi.example.com        |
                          |                                                                                           |
                          |                                                                                           |
               ---        V                                                                                           V
              |       --------  <-------- 1. Send signed SSL certificate --------------------------------  -------------------
   SSL        |      |  gRPC  | ------*                                                                   |   gRPC Server     |
Handshake     |      | Client | <----/    2. Verify SSL certificate from Server                           |                   |
              |      |        |                                                                           | myapi.example.com |
              |       --------  <======== 3. Secure SSL Encrypted Communication ========================>  -------------------
               ---
```

* i. Certificate Authority (CA): can be public if you want to assign a public URL (e.g. myapi.example.com); or you can have a private CA (e.g. internal URLs), in which case, you have to create or maintain that CA.
* ii. server can create a private key (server PEM Private Key)
  * by using the private key, it will generate a certificate request
  * basically, it'll ask CA for signing the certificate request
  * thus, CA gives signed certificate (`server.crt` is a certificate that's signed by CA)
    * server-side, we need to have
      * a private key
      * signed certificate
* iii. client-side needs "trust certificate" from the CA
  * CA usually issues "CA Root Public Certificate"
* iv. now, it's ready to do SSL Handshake
  * send signed SSL certificate
  * verify SSL certificate from server
  * secure SSL encrypted communication

> Wow, it's a LOT...

but gRPC makes things simpler.

---

## 48. [Hands-On] SSL Encryption in gRPC [Golang]

* We'll setup
  * a certificate autority (CA)
  * a server certificate
* We'll sign
  * a server certificate

then,

* We'll setup
  * the Server to use TLS
  * the Client to connect securely over TLS

* links:
  * https://github.com/grpc/grpc-go/blob/master/Documentation/grpc-auth-support.md
  + https://grpc.io/docs/guides/auth.html

### 48.1. Looking at the gRPC Official Documentation

Go code:

* **base case - no encryption or authentication**
  * client:

    ```go
    conn, _ := grpc.Dial("localhost:50051", grpc.WithInsecure())
    // error handling omitted
    client := pb.NewGreeterClient(conn)
    // ...
    ```

  * server:

    ```go
    s := grpc.NewServer()
    lis, _ := net.Listen("tcp", "localhost:50051")
    // error handling omitted
    s.Serve(lis)
    ```

* **with server authentication SSL/TLS**
  * client:

    ```go
    creds := credentials.NewClientTLSFromFile(certFile, "")
    conn, _ := grpc.Dial("localhost:50051", grpcWithTransportCredentials(creds))
    // error handling omitted
    client := pb.NewGreeterClient(conn)
    // ...
    ```
  
  * server:
  
    ```go
    creds := credentials.NewServerTLSFromFile(certFile, keyFile)
    s := grpc.NewServer(grpc.Creds(creds))
    lis, _ := net.Listen("tcp", "localhost:50051")
    // error handling omitted
    s.Serve(lis)
    ```

### 48.2. SSL Encryption Keys Generation

* let's add `ssl` directory at the same level as `calculator` and `greet` directories

```note
calculator/
  calculator_client/...
  calculator_server/...
  calculatorpb/...

greet/
  greet_client/...
  greet_server/...
  greetpb/...

ssl/
  instructions.sh

generation.sh
```

and in the `instructions.sh` we have this code:

```sh
#!/bin/bash
# Inspired from: https://github.com/grpc/grpc-java/tree/master/examples#generating-self-signed-certificates-for-use-with-grpc

# Output files
# ca.key: Certificate Authority private key file (this shouldn't be shared in real-life)
# ca.crt: Certificate Authority trust certificate (this should be shared with users in real-life)
# server.key: Server private key, password protected (this shouldn't be shared)
# server.csr: Server certificate signing request (this should be shared with the CA owner)
# server.crt: Server certificate signed by the CA (this would be sent back by the CA owner) - keep on server
# server.pem: Conversion of server.key into a format gRPC likes (this shouldn't be shared)

# Summary
# Private files: ca.key, server.key, server.pem, server.crt
# "Share" files: ca.crt (needed by the client), server.csr (needed by the CA)

# Changes these CN's to match your hosts in your environment if needed.
SERVER_CN=localhost

# Step 1: Generate Certificate Authority + Trust Certificate (ca.crt)
openssl genrsa -passout pass:1111 -des3 -out ca.key 4096
openssl req -passin pass:1111 -new -x509 -days 3650 -key ca.key -out ca.crt -subj "/CN=${SERVER_CN}"

# Step 2: Generate the Server Private Key (server.key)
openssl genrsa -passout pass:1111 -des3 -out server.key 4096

# Step 3: Get a certificate signing request from the CA (server.csr)
openssl req -passin pass:1111 -new -key server.key -out server.csr -subj "/CN=${SERVER_CN}"

# Step 4: Sign the certificate with the CA we created (it's called self signing) - server.crt
openssl x509 -req -passin pass:1111 -days 3650 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt 

# Step 5: Convert the server certificate to .pem format (server.pem) - usable by gRPC
openssl pkcs8 -topk8 -nocrypt -passin pass:1111 -in server.key -out server.pem
```

* `SERVER_CN` is not set as `localhost
  * but, if you are running it with the real API address you can change that
  * e.g. `SERVER_CN=myapi.example.com`

open your terminal and do this one by one:

```bash
SERVER_CN=localhost
```

check it is set well:

```bash
$ echo $SERVER_CN
localhost
```

go into directory `ssl`:

```bash
cd ssl
$ pwd
/.../ssl
```

* Step 1: Generate Certificate Authority + Trust Certificate (ca.crt)
  * create CA by using this command, output would be `ca.key`:
  * also get `ca.crt`

  ```bash
  $ openssl genrsa -passout pass:1111 -des3 -out ca.key 4096
  Generating RSA private key, 4096 bit long modulus
  ....................................................................................................................................................++
  ..................................................................................................................++
  e is 65537 (0x10001)
  ```

  then you get `ca.key` as well:

  ```bash
  $ ls
  ca.key
  instructions.sh
  ```

  now let's run this command (currently `SERVER_CN` is `localhost`):

  ```bash
  $ openssl req -passin pass:1111 -new -x509 -days 3650 -key ca.key -out ca.crt -subj "/CN=${SERVER_CN}"
  $ ls
  ca.crt
  ca.key
  instructions.sh
  ```

* Step 2: Generate the Server Private Key (`server.key`)

  ```bash
  $ openssl genrsa -passout pass:1111 -des3 -out server.key 4096
  Generating RSA private key, 4096 bit long modulus
  ...++
  ....................................................................................................................................................................................++
  e is 65537 (0x10001)

  $ ls
  ca.crt
  ca.key
  instructions.sh
  server.key
  ```

* Step 3: Get a certificate signing request from the CA (`server.csr`)

  ```bash
  $ openssl req -passin pass:1111 -new -key server.key -out server.csr -subj "/CN=${SERVER_CN}"

  $ ls
  ca.crt
  ca.key
  instructions.sh
  server.csr
  server.key
  ```

* Step 4: Sign the certificate with the CA we created (it's called self signing) - `server.crt`

  ```bash
  $ openssl x509 -req -passin pass:1111 -days 3650 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt
  Signature ok
  subject=/CN=localhost
  Getting CA Private Key

  $ ls
  ca.crt
  ca.key
  instructions.sh
  server.crt
  server.csr
  server.key
  ```

* Step 5: Convert the server certificate to .pem format (`server.pem`) - usable by gRPC

  ```bash
  $ openssl pkcs8 -topk8 -nocrypt -passin pass:1111 -in server.key -out server.pem

  $ ls
  ca.crt
  ca.key
  instructions.sh
  server.crt
  server.csr
  server.key
  server.pem
  ```

### 48.3. Use the Keys to `greet` example

let's go to `greet` project's `greet/greet_server/server.go`.  

What we have to do is, like we saw from the [gRPC documentation](https://grpc.io/docs/guides/auth.html#go), we may want to consider this:

* With server authentication SSL/TLS
  * Client:

    ```go
    creds, _ := credentials.NewClientTLSFromFile(certFile, "")
    conn, _ := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(creds))
    // error handling omitted
    client := pb.NewGreeterClient(conn)
    // ...
    ```

  * Server:

    ```go
    creds, _ := credentials.NewServerTLSFromFile(certFile, keyFile)
    s := grpc.NewServer(grpc.Creds(creds))
    lis, _ := net.Listen("tcp", "localhost:50051")
    // error handling omitted
    s.Serve(lis)
    ```

#### 48.3.1 Server

We need to create a credential, `NewServerTLSFromFile(certFile, keyFile)` and specify two files (`certFile`, `keyFile`). Thus, let's go back to `greet/greet_server/server.go`

```go
func main() {
  fmt.Println("Hello world!")

  lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
  if err != nil {
    log.Fatalf("Failed to listen: %v", err)
  }

  certFile, keyFile := "ssl/server.crt", "ssl/server.pem"
  creds, sslErr := credentials.NewServerTLSFromFile(certFile, keyFile)
  if sslErr != nil {
    log.Fatalf("Failed loading certificates: %v", sslErr)
  }
  opts := grpc.Creds(creds)

  s := grpc.NewServer(opts)
  greetpb.RegisterGreetServiceServer(s, &server{})

  if err := s.Serve(lis); err != nil {
    log.Fatalf("Failed to serve: %v", err)
  }
}
```

so, we defined the `certFile` and `keyFile`, then get `creds` by using two files via `credentials.NewServerTLSFromFile()`. Set the `opts` by using `creds` via `grpc.Creds()` and put it into `grpc.NewServer()`.

Now, we can run the server to make sure it's SSL enabled:

```bash
$ go run greet/greet_server/server.go 
Hello world!
```

It's running so it seems okay now and let's try to run client and modify the client.

#### 48.3.2 Client

Now, we can add SSL to client code (`greet/greet_client/client.go`). This time, let's use `doUnary(c)`

```go
func main() {
  fmt.Println("Hello, I am a client.")

  cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure()) // WithInsecure() for just now testing
  if err != nil {
    log.Fatalf("Could not connect: %v", err)
  }

  defer cc.Close()

  c := greetpb.NewGreetServiceClient(cc)
  // fmt.Printf("Created client: %f", c)

  doUnary(c)
  // doServerStreaming(c)
  // doClientStreaming(c)
  // doBiDiStreaming(c)

  // doUnaryWithDeadline(c, 5*time.Second) // should complete
  // doUnaryWithDeadline(c, 1*time.Second) // should timeout
}

func doUnary(c greetpb.GreetServiceClient) {
  fmt.Println("Starting to do a Unary RPC...")
  req := &greetpb.GreetRequest{
    Greeting: &greetpb.Greeting{
      FirstName: "Mark",
      LastName:  "Hahn",
    },
  }
  res, err := c.Greet(context.Background(), req)
  if err != nil {
    log.Fatalf("error while calling Greet RPC: %v", err)
  }
  log.Printf("Response from Greet: %v", res.Result)
}
```

pay attention of this part:

```go
cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure()) // WithInsecure() for just now testing
```

as we are using `grpc.WithInsecure()`, we can try to run this client.
Since the server is running, we can run the client right now in another terminal:

```bash
$ go run greet/greet_client/client.go
Hello, I am a client.
Starting to do a Unary RPC...
2020/03/27 18:53:53 error while calling Greet RPC: rpc error: code = Unavailable desc = connection closed
exit status 1
```

and you can see the server's screen (nothing changed, just showing the same screen as sam as when we ran the code at the previous section):

```bash
$ go run greet/greet_server/server.go
Hello world!
```

So, client-side got error message and the server side has no additional message.

**Thus, we DO need to change our client-side code:**

* remember the sample code that gRPC docs shows

```go
creds := credentials.NewClient(certiFile, "")
conn, _ := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(creds))
// error handling omitted
client := pb.NewGreeterClient(conn)
//...
```

let's revisit the code:

```go
func main() {
  fmt.Println("Hello, I am a client.")

  certFile := "ssl/ca.crt" // Certificate Authority Trust certificate
  creds, sslErr := credentials.NewClientTLSFromFile(certFile, "") // the 2nd argument is override of the server name
  if sslErr != nil {
    log.Fatalf("Error whilst loading CA trust certificate: %v", sslErr)
  }
  opts := grpc.WithTransportCredentials(creds)
  // cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure()) // WithInsecure() for just now testing
  cc, err := grpc.Dial("localhost:50051", opts)
  if err != nil {
    log.Fatalf("Could not connect: %v", err)
  }

  defer cc.Close()

  c := greetpb.NewGreetServiceClient(cc)
  // fmt.Printf("Created client: %f", c)

  doUnary(c)
  // doServerStreaming(c)
  // doClientStreaming(c)
  // doBiDiStreaming(c)

  // doUnaryWithDeadline(c, 5*time.Second) // should complete
  // doUnaryWithDeadline(c, 1*time.Second) // should timeout
}

func doUnary(c greetpb.GreetServiceClient) {
  fmt.Println("Starting to do a Unary RPC...")
  req := &greetpb.GreetRequest{
    Greeting: &greetpb.Greeting{
      FirstName: "Mark",
      LastName:  "Hahn",
    },
  }
  res, err := c.Greet(context.Background(), req)
  if err != nil {
    log.Fatalf("error while calling Greet RPC: %v", err)
  }
  log.Printf("Response from Greet: %v", res.Result)
}
```

now, we can run the client again:

```bash
$ go run greet/greet_client/client.go 
Hello, I am a client.
Starting to do a Unary RPC...
2020/03/27 22:29:23 Response from Greet: Hello Mark
```

and see the result printed out, and the server-side also get this message:

```bash
Greet function was invoked with greeting:<first_name:"Mark" last_name:"Hahn" >
```

---

#### 48.3.3. Small Refactoring

* **server-side**

  ```go
  func main() {
    fmt.Println("Hello world!")

    lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
    if err != nil {
      log.Fatalf("Failed to listen: %v", err)
    }

    var opts grpc.ServerOption

    tls := false  // or `tls := true`
    if tls {
      certFile, keyFile := "ssl/server.crt", "ssl/server.pem"
      creds, sslErr := credentials.NewServerTLSFromFile(certFile, keyFile)
      if sslErr != nil {
        log.Fatalf("Failed loading certificates: %v", sslErr)
      }
      opts := grpc.Creds(creds)
    }

    s := grpc.NewServer(opts)
    greetpb.RegisterGreetServiceServer(s, &server{})

    if err := s.Serve(lis); err != nil {
      log.Fatalf("Failed to serve: %v", err)
    }
  }
  ```

  run the server:

  ```bash
  $ go run greet/greet_server/server.go 
  Hello world!
  panic: runtime error: invalid memory address or nil pointer dereference
  [signal SIGSEGV: segmentation violation code=0x1 addr=0x18 pc=0x13f5d42]

  goroutine 1 [running]:
  google.golang.org/grpc.NewServer(0xc0000fff30, 0x1, 0x1, 0xd)
  ...
  ```

  but with this code, we get `nil pointer reference error, so we need to change

  ```go
  var opt grpc.ServerOption
  // ...
  if tls {
    // ...
    opts = grpc.Creds(creds))
  }

  s := grpc.NewServer(opts)
  // ...
  ```

  to

  ```go
  opts := []grpc.ServerOption
  // ...
  if tls {
    // ...
    opts = append(opts, grpc.Creds(creds))
  }

  s := grpc.NewServer(opts...)
  // ...
  ```

  so it should look like this:

  ```go
  func main() {
    fmt.Println("Hello world!")

    lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
    if err != nil {
      log.Fatalf("Failed to listen: %v", err)
    }

    opts := []grpc.ServerOption{}
    tls := false
    if tls {
      certFile, keyFile := "ssl/server.crt", "ssl/server.pem"
      creds, sslErr := credentials.NewServerTLSFromFile(certFile, keyFile)
      if sslErr != nil {
        log.Fatalf("Failed loading certificates: %v", sslErr)
      }
      opts = append(opts, grpc.Creds(creds))
    }

    s := grpc.NewServer(opts...)
    greetpb.RegisterGreetServiceServer(s, &server{})

    if err := s.Serve(lis); err != nil {
      log.Fatalf("Failed to serve: %v", err)
    }
  }
  ```

  and run the server again:

  ```bash
  $ go run greet/greet_server/server.go
  Hello world!
  ```

  now the server is running well, let's fix the client.

* **client-side**

```go
func main() {
  fmt.Println("Hello, I am a client.")

  tls := false  // or `tls := true`
  opts := grpc.WithInsecure()
  if tsl {
    certFile := "ssl/ca.crt" // Certificate Authority Trust certificate
    creds, sslErr := credentials.NewClientTLSFromFile(certFile, "") // the 2nd argument is override of the server name
    if sslErr != nil {
      log.Fatalf("Error whilst loading CA trust certificate: %v", sslErr)
    }
    opts := grpc.WithTransportCredentials(creds)
  }

  cc, err := grpc.Dial("localhost:50051", opts)
  if err != nil {
    log.Fatalf("Could not connect: %v", err)
  }

  defer cc.Close()

  c := greetpb.NewGreetServiceClient(cc)
  // fmt.Printf("Created client: %f", c)

  doUnary(c)
  // doServerStreaming(c)
  // doClientStreaming(c)
  // doBiDiStreaming(c)

  // doUnaryWithDeadline(c, 5*time.Second) // should complete
  // doUnaryWithDeadline(c, 1*time.Second) // should timeout
}

func doUnary(c greetpb.GreetServiceClient) {
  fmt.Println("Starting to do a Unary RPC...")
  req := &greetpb.GreetRequest{
    Greeting: &greetpb.Greeting{
      FirstName: "Mark",
      LastName:  "Hahn",
    },
  }
  res, err := c.Greet(context.Background(), req)
  if err != nil {
    log.Fatalf("error while calling Greet RPC: %v", err)
  }
  log.Printf("Response from Greet: %v", res.Result)
}
```

client can be run:

```bash
$ go run greet/greet_client/client.go
Hello, I am a client.
Starting to do a Unary RPC...
2020/03/29 00:29:58 Response from Greet: Hello Mark
```

**Also, we can enable the TLS mode** to client and server side

```go
tls := true
```

and run the server:

```bash
$ go run greet/greet_server/server.go 
Hello world!
```

here is the client code:

```go
func main() {
  fmt.Println("Hello world!")

  lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
  if err != nil {
    log.Fatalf("Failed to listen: %v", err)
  }

  opts := []grpc.ServerOption{}
  tls := true
  if tls {
    certFile, keyFile := "ssl/server.crt", "ssl/server.pem"
    creds, sslErr := credentials.NewServerTLSFromFile(certFile, keyFile)
    if sslErr != nil {
      log.Fatalf("Failed loading certificates: %v", sslErr)
    }
    opts = append(opts, grpc.Creds(creds))
  }

  s := grpc.NewServer(opts...)
  greetpb.RegisterGreetServiceServer(s, &server{})

  if err := s.Serve(lis); err != nil {
    log.Fatalf("Failed to serve: %v", err)
  }
}
```

and run the client again:

```bash
$ go run greet/greet_client/client.go 
Hello, I am a client.
Starting to do a Unary RPC...
2020/03/29 02:28:34 Response from Greet: Hello Mark
```

then the server get this message:

```bash
Greet function was invoked with greeting:<first_name:"Mark" last_name:"Hahn" > 
```

---

## 49. [Demo] Language Interoperability

* gPRC can be used by any language
  * because the code can be generated for any language,
  * it makes it super simple to create micro-services in any language that interact with each other

```note
                                            -----------------                    ----------
                                           | Purchase  ------|  proto req/res   | Shipment |
   --------------------    proto req/res   | Service  | stub | ---------------> | Service  |
  |                    | /---------------> | (Go)      ------|                  | (C#)     |
  |              ------|/                   -----------------                    ----------
  | Mobile App  | stub |
  | (Java)       ------|\                   ----------
  |                    | \---------------> | Pricing  |
   --------------------|   proto req/res   | Service  |
                                           | (Python) |
                                            ----------
```

* Therefore we can do this:
  * have a protobuf file
    * create proto to go file
    * create proto to java file
  * write go server and run it
  * write java client and run it
  * vice versa
  * or with other languages

---

## 50.gRPC Reflection & Evans CLI

### 50.1. gRPC Reflection & CLI

* As we've seen, for Clients to connect to our Server,
  * they need to have a `.proto` file
    * which defines the service
* This is fine for production (you definitely want to know the API definition in advance)
* For development, when you have a gRPC server you don't know, sometimes you wish you could ask the server:
  * > "what APIs do you have?"
* That's reflection!
* We may want reflection for two reasons:
  * Having servers "expose" which endpoints are available
  * Allowing **command line interface (CLI)** to talk to our server without have a preliminary `.proto` file
* Let's implement Reflection on our Server
* We'll use the **evans** CLI to practice on the client side

### 50.2. Reflection on gPRC package

* visit [github.com/grpc/grpc-go](https://www.github.com/grpc/grpc-go)
  * go to [reflection](https://github.com/grpc/grpc-go/tree/master/reflection)
  * it shows:
    * Package reflection implements server reflection service.
    * The service implemented is defined in: https://github.com/grpc/grpc/blob/master/src/proto/grpc/reflection/v1alpha/reflection.proto.
    * To register server reflection on a gRPC server:

      ```go
      import "google.golang.org/grpc/reflection"

      s := grpc.NewServer()
      pb.RegisterYourOwnServer(s, &server{})

      // Register reflection service on gRPC server.
      reflection.Register(s)

      s.Serve(lis)
      ```

### 50.3. Reflection Hands-on with `calculator`

* let's try this on: `calculator/calculator_server/server.go`
  * what we have to do:
    * import `google.golang.org/grpc/reflection`
    * use `reflection.Register(s)` where `s := grpc.NewServer()`

```go
package main

import (
  // ...
  "google.golang.org/grpc/reflection"
  // ...
)

// ...

func main() {
  fmt.Println("Calculator Server")

  lis, err := net.Listen("tcp", "0.0.0.0:50051")
  if err != nil {
    log.Fatalf("Failed to listen: %v", err)
  }

  s := grpc.NewServer()
  calculatorpb.RegisterCalculatorServiceServer(s, &server{})

  // Register reflection service on gRPC server.
  reflection.Register(s)

  if err := s.Serve(lis); err != nil {
    log.Fatalf("Failed to server: %v", err)
  }
}
```

and run the server:

```bash
$ go run calculator/calculator_server/server.go
Calculator Server
```

### 50.4. Evans CLI

* Evans CLI: [github.com/ktr0731/evans](https://github.com/ktr0731/evans)
* instal
  * MacOS

```bash
$ brew tap ktr0731/evans
$ brew install evans
```

try to run it:

```bash
$ evans
evans 0.8.5

Usage: evans [--help] [--version] [options ...] [PROTO [PROTO ...]]

Positional arguments:
        PROTO                          .proto files

Options:
        --silent, -s                     hide redundant output (default "false")
        --package string                 default package
        --service string                 default service
        --path strings                   proto file paths (default "[]")
        --host string                    gRPC server host
        --port, -p string                gRPC server port (default "50051")
        --header slice of strings        default headers that set to each requests (example: foo=bar) (default "[]")
        --web                            use gRPC-Web protocol (default "false")
        --reflection, -r                 use gRPC reflection (default "false")
        --tls, -t                        use a secure TLS connection (default "false")
        --cacert string                  the CA certificate file for verifying the server
        --cert string                    the certificate file for mutual TLS auth. it must be provided with --certkey.
        --certkey string                 the private key file for mutual TLS auth. it must be provided with --cert.
        --servername string              override the server name used to verify the hostname (ignored if --tls is disabled)
        --edit, -e                       edit the project config file by using $EDITOR (default "false")
        --edit-global                    edit the global config file by using $EDITOR (default "false")
        --verbose                        verbose output (default "false")
        --version, -v                    display version and exit (default "false")
        --help, -h                       display help text and exit (default "false")

evans: invalid config condition: 1 error occurred:

* one or more proto files, or gRPC reflection required
```

try this: `evans -p 50051 -r` (evans with port 50051 by using gRPC reflection)

```bash
$ evans -p 50051 -r

  ______
 |  ____|
 | |__    __   __   __ _   _ __    ___
 |  __|   \ \ / /  / _. | | '_ \  / __|
 | |____   \ V /  | (_| | | | | | \__ \
 |______|   \_/    \__,_| |_| |_| |___/

 more expressive universal gRPC client


calculator.CalculatorService@127.0.0.1:50051>
```

shwo package:

```bash
calculator.CalculatorService@127.0.0.1:50051> show package
+------------+
|  PACKAGE   |
+------------+
| calculator |
+------------+
```

show service:

```bash
calculator.CalculatorService@127.0.0.1:50051> show service
+-------------------+--------------------------+---------------------------------+----------------------------------+
|      SERVICE      |           RPC            |          REQUEST TYPE           |          RESPONSE TYPE           |
+-------------------+--------------------------+---------------------------------+----------------------------------+
| CalculatorService | Sum                      | SumRequest                      | SumResponse                      |
| CalculatorService | PrimeNumberDecomposition | PrimeNumberDecompositionRequest | PrimeNumberDecompositionResponse |
| CalculatorService | ComputeAverage           | ComputeAverageRequest           | ComputeAverageResponse           |
| CalculatorService | FindMaximum              | FindMaximumRequest              | FindMaximumResponse              |
| CalculatorService | SquareRoot               | SquareRootRequest               | SquareRootResponse               |
+-------------------+--------------------------+---------------------------------+----------------------------------+
```

show message:

```bash
calculator.CalculatorService@127.0.0.1:50051> show message
+----------------------------------+
|             MESSAGE              |
+----------------------------------+
| ComputeAverageRequest            |
| ComputeAverageResponse           |
| FindMaximumRequest               |
| FindMaximumResponse              |
| PrimeNumberDecompositionRequest  |
| PrimeNumberDecompositionResponse |
| SquareRootRequest                |
| SquareRootResponse               |
| SumRequest                       |
| SumResponse                      |
+----------------------------------+
```

desc (description) for `SumRequest`:

```bash
calculator.CalculatorService@127.0.0.1:50051> desc SumRequest
+---------------+------------+----------+
|     FIELD     |    TYPE    | REPEATED |
+---------------+------------+----------+
| first_number  | TYPE_INT32 | false    |
| second_number | TYPE_INT32 | false    |
+---------------+------------+----------+
```

call `Sum` RPC:

```bash
calculator.CalculatorService@127.0.0.1:50051> call Sum
first_number (TYPE_INT32) => 12
second_number (TYPE_INT32) => 32
{
  "sumResult": 44
}
```

call `PrimeNumberDecomposition` RPC:

```bash
calculator.CalculatorService@127.0.0.1:50051> call PrimeNumberDecomposition
number (TYPE_INT64) => 12321
{
  "primeFactor": "3"
}
{
  "primeFactor": "3"
}
{
  "primeFactor": "37"
}
{
  "primeFactor": "37"
}
```

call `ComputeAverage` RPC: (it's streaming, so when you want to quit, you have to enter `control + d` as a shutdown signal)

```bash
number (TYPE_INT32) => 1
number (TYPE_INT32) => 2
number (TYPE_INT32) => 3
number (TYPE_INT32) => 23
number (TYPE_INT32) => 114
number (TYPE_INT32) => 534534
number (TYPE_INT32) => 
{
  "average": 89112.83333333333
}
```

call `FindMaximum` RPC:

```bash
calculator.CalculatorService@127.0.0.1:50051> call FindMaximum
number (TYPE_INT32) => 3
number (TYPE_INT32) => {
  "maximum": 3
}
number (TYPE_INT32) => 4
number (TYPE_INT32) => {
  "maximum": 4
}
number (TYPE_INT32) => 2
number (TYPE_INT32) => 6
number (TYPE_INT32) => {
  "maximum": 6
}
number (TYPE_INT32) => 10
number (TYPE_INT32) => {
  "maximum": 10
}
number (TYPE_INT32) => 
```

call `SquareRoot` RPC:

```bash
calculator.CalculatorService@127.0.0.1:50051> call SquareRoot
number (TYPE_INT32) => 400
{
  "numberRoot": 20
}

calculator.CalculatorService@127.0.0.1:50051> call SquareRoot
number (TYPE_INT32) => -42
command call: failed to send a request: rpc error: code = InvalidArgument desc = Received a negative number: -42
```

---
