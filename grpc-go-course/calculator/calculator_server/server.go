package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net"

	cpb "../calculatorpb"
	grpc "google.golang.org/grpc"
)

type server struct{}

// takes the first and second number from the request and returns their sum
func (*server) Sum(ctx context.Context, req *cpb.Request) (*cpb.Response, error) {
	fmt.Printf("Sum function invoked with %v\n", req)
	first := req.GetFirst()
	second := req.GetSecond()
	res := &cpb.Response{
		Sum: first + second,
	}

	return res, nil
}

// Streaming server
// Takes in a number and return a stream of its prime factors
func (*server) PrimeNumberDecomposition(req *cpb.PrimeNumberDecompositionRequest, stream cpb.CalculatorService_PrimeNumberDecompositionServer) error {
	fmt.Printf("PrimeNumberDecomposition function invoked with %v\n", req)
	k := int64(2)
	number := req.GetNumber()
	for number > 1 {
		if number%k == 0 {
			res := &cpb.PrimeNumberDecompositionResponse{
				PrimeFactor: k,
			}
			stream.Send(res)
			number = number / k
		} else {
			k = k + 1
			fmt.Printf("k has increased to %v\n", k)
		}
	}
	return nil
}

// Client streaming
// Takes in a stream of number and returns the average of all numbers in the request
func (*server) ComputeAverage(stream cpb.CalculatorService_ComputeAverageServer) error {
	fmt.Printf("ComputeAverage function was invoked with a streaming request\n")

	count := int64(0)
	total := int64(0)
	result := int64(0)

	for {
		req, err := stream.Recv()
		if err == io.EOF {
			// done reading incoming stream
			return stream.SendAndClose(&cpb.ComputeAverageResponse{
				Average: result,
			})
		}
		if err != nil {
			log.Fatalf("Error whilst reading client stream: %v", err)
		}
		count++
		fmt.Println("Count is now: %v\n", count)
		total = total + req.GetNumber()
		fmt.Println("Total is now: %v\n", total)
		result = total / count
	}
}

func main() {
	fmt.Println("Calculator server running...")

	lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := grpc.NewServer()
	cpb.RegisterCalculatorServiceServer(s, &server{})

	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
