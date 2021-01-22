package main

import (
	"context"
	"fmt"
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

	doSum(c)
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
