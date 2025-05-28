package database

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/redis/go-redis/v9"
)

var (
	RedisClient *redis.Client
	Ctx         = context.Background()
)


// ConnectRedis initializes a Redis client
func ConnectRedis() error {

	port := os.Getenv("REDIS_PORT")
	redis_password := os.Getenv("REDIS_PASSWORD")
	host := os.Getenv("REDIS_HOST")
	address := fmt.Sprintf("%s:%s", host, port)

	RedisClient = redis.NewClient(&redis.Options{
		Addr:     address, // Default Redis address
		Password: redis_password,               // No password (unless set in Redis config)
		DB:       0,                // Use default database (change if needed)
	})

	// Test connection
	_, err := RedisClient.Ping(Ctx).Result()
	if err != nil {
		log.Fatalf("❌ Failed to connect to Redis: %v", err)
		return err
	}

	fmt.Println("✅ Connected to Redis on localhost:6379")
	return nil
}
