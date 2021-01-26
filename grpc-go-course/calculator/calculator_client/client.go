package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"time"

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
	// doPrimeNumberDecomposition(c)
	// doComputeAverage(c)
	doFindMaximum(c)
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

// Server Streaming
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

// Client Streaming
func doComputeAverage(c cpb.CalculatorServiceClient) {
	fmt.Println("Computing average Client Streaming RPC...")

	stream, err := c.ComputeAverage(context.Background())
	if err != nil {
		log.Fatalf("error whlist calling ComputeAverage: %v", err)
	}

	numbers := []int32{3, 5, 9, 54, 23}

	for _, num := range numbers {
		fmt.Printf("Sending number: %v\n", num)
		stream.Send(&cpb.ComputeAverageRequest{
			Number: num,
		})
	}

	res, err := stream.CloseAndRecv()
	if err != nil {
		log.Fatalf("error whilst receiving response from ComputeAverage: %v", err)
	}

	fmt.Printf("ComputeAverage Response: %v\n", res.GetAverage())
}

// Bi-directional Streaming
func doFindMaximum(c cpb.CalculatorServiceClient) {
	fmt.Println("Starting to do a BiDi Streaming RPC...")

	stream, err := c.FindMaximum(context.Background())
	if err != nil {
		log.Fatalf("Error whilst creating stream: %v", err)
	}

	waitc := make(chan struct{})

	// sending
	go func() {
		numbers := []int32{4, 7, 2, 19, 4, 6, 32}

		for _, number := range numbers {
			fmt.Printf("Sending message: %v\n", number)
			stream.Send(&cpb.FindMaximumRequest{
				Number: number,
			})
			time.Sleep(1000 * time.Millisecond)
		}
		stream.CloseSend()
	}()

	// receiving
	go func() {
		for {
			res, err := stream.Recv()
			if err == io.EOF {
				break
			}
			if err != nil {
				log.Fatalf("Error whilst receiving: %v", err)
				break
			}
			fmt.Printf("Received a new maximum: %v\n", res.GetMaximum())
		}

		close(waitc)
	}()

	// block until everyone is done
	<-waitc
}
