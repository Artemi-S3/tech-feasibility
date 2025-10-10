package main

import (
	"context"
	"fmt"
	"io"
	"strings"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	s3types "github.com/aws/aws-sdk-go-v2/service/s3/types"
	"github.com/aws/aws-sdk-go-v2/feature/s3/manager"
	"github.com/aws/aws-sdk-go-v2/feature/s3/presign"
)

func main() {
  ctx := context.Background()
  cfg, err := config.LoadDefaultConfig(ctx)
  if err != nil { panic(err) }
  client := s3.NewFromConfig(cfg)

  // list buckets
  lb, err := client.ListBuckets(ctx, &s3.ListBucketsInput{})
  if err != nil { panic(err) }
  for _, b := range lb.Buckets { fmt.Println(*b.Name) }

  bucket := "my-bucket"
  key := "go-demo/hello.txt"

  // upload small text
  _, err = client.PutObject(ctx, &s3.PutObjectInput{
    Bucket: aws.String(bucket),
    Key:    aws.String(key),
    Body:   strings.NewReader("hello from go"),
  })
  if err != nil { panic(err) }

  // download
  out, err := client.GetObject(ctx, &s3.GetObjectInput{
    Bucket: aws.String(bucket),
    Key:    aws.String(key),
  })
  if err != nil { panic(err) }
  body, _ := io.ReadAll(out.Body)
  fmt.Println(string(body))
  out.Body.Close()

  // presigned URL
  p := presign.NewPresignClient(client)
  presigned, err := p.PresignGetObject(ctx, &s3.GetObjectInput{
    Bucket: aws.String(bucket),
    Key:    aws.String(key),
  }, s3.WithPresignExpires(5*time.Minute))
  if err != nil { panic(err) }
  fmt.Println(presigned.URL)
}
