package main

import (
	"fmt"
	"log"
	"net"

	"../greetpb"
	grpc "google.golang.org/grpc"
)

type server struct{}

func main() {
	fmt.Println("Hello world!")

	lis, err := net.Listen("tcp", "0.0.0.0:50051") // 50051 is a default port for gRPC
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := grpc.NewServer()
	greetpb.RegisterGreetServiceServer(s, &server{})

	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
