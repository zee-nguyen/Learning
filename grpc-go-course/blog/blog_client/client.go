package main

import (
	"context"
	"fmt"
	"log"

	"google.golang.org/grpc"

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

	// Create blog
	fmt.Println("Creating the blog...")
	blog := &blogpb.Blog{
		AuthorId: "Zee",
		Title:    "My First Blog",
		Content:  "Content of first blog",
	}

	createBlogRes, err := c.CreateBlog(context.Background(), &blogpb.CreateBlogRequest{Blog: blog})
	if err != nil {
		log.Fatalf("Unexpected err: %v", err)
	}
	fmt.Printf("Blog has been created: %v", createBlogRes)
	blogID := createBlogRes.GetBlog().GetId()

	// Read Blog
	fmt.Println("Reading the blog...")

	// BlogId got from the first call call to create a blog item
	_, err2 := c.ReadBlog(context.Background(), &blogpb.ReadBlogRequest{BlogId: "601044f5a60c4b7c732e93c8"})
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
