package main

import (
	"context"
	"fmt"
	"io"
	"log"

	cpb "../calculatorpb"
	grpc "google.golang.org/grpc"
)

func main() {
	fmt.Println("Bonjour, je suis un client.")

	cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure()) // WithInsecure() for just now testing
	if err != nil {
		log.Fatalf("Could not connect: %v", err)
	}

	defer cc.Close()

	c := cpb.NewCalculatorServiceClient(cc)

	// doSum(c)
	doPrimeNumberDecomposition(c)
}

func doSum(c cpb.CalculatorServiceClient) {
	fmt.Println("doing sum...")

	req := &cpb.Request{
		First:  5,
		Second: 10,
	}

	res, err := c.Sum(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling Calculator RPC: %v", err)
	}

	log.Printf("Response from Calculator: %v", res.Sum)
}

func doPrimeNumberDecomposition(c cpb.CalculatorServiceClient) {
	fmt.Println("Doing prime number decompos Server Streaming RPC...")

	// building a request
	req := &cpb.PrimeNumberDecompositionRequest{
		Number: 35135442,
	}

	resStream, err := c.PrimeNumberDecomposition(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling Calculator RPC: %v", err)
	}

	// iterate through stream response
	for {
		msg, err := resStream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("error whilst reading stream: %v", err)
		}

		log.Printf("Response from DoPrimeNumberDecomposition: %v", msg.GetPrimeFactor())
	}
}
