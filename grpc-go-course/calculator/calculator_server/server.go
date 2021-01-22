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
	fmt.Println("Sum function invoked with %v\n", req)
	first := req.GetFirst()
	second := req.GetSecond()
	res := &cpb.Response{
		Sum: first + second,
	}

	return res, nil
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
