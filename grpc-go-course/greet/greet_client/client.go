package main

import (
	"context"
	"fmt"
	"io"
	"log"

	greetpb "../greetpb"
	grpc "google.golang.org/grpc"
)

func main() {
	fmt.Println("Bonjour, je suis un client.")

	cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure()) // WithInsecure() for just now testing
	if err != nil {
		log.Fatalf("Could not connect: %v", err)
	}

	defer cc.Close()

	c := greetpb.NewGreetServiceClient(cc)
	// fmt.Printf("Created client: %f", c)

	// doUnary(c)
	doServerStreaming(c)
}

func doUnary(c greetpb.GreetServiceClient) {
	fmt.Println("Starting to do a Unary RPC...")
	// build a simple GreetRequest
	req := &greetpb.GreetRequest{
		Greeting: &greetpb.Greeting{
			FirstName: "Bon",
			LastName:  "Jour",
		},
	}
	res, err := c.Greet(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling Greet RPC: %v", err)
	}
	log.Printf("Response from Greet: %v", res.Result)
}

func doServerStreaming(c greetpb.GreetServiceClient) {
	fmt.Println("Starting to do a Server Streaming RPC...")

	// building a request
	req := &greetpb.GreetManyTimesRequest{
		Greeting: &greetpb.Greeting{
			FirstName: "Bon",
			LastName:  "Jour",
		},
	}

	// sending the request
	resStream, err := c.GreetManyTimes(context.Background(), req)
	if err != nil {
		log.Fatal("error whilst calling GreetManyTimes RPC: %v", err)
	}

	// iterate through the stream response
	for {
		msg, err := resStream.Recv()
		if err == io.EOF {
			// we've reached the end of the stream
			break
		}
		if err != nil {
			log.Fatal("error whilst reading stream: %v", err)
		}

		log.Printf("Response from GreetManyTimes: %v", msg.GetResult())
	}
}
