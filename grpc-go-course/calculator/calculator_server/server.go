package main

import (
	"context"
	"fmt"
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
