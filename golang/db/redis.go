package database

import (
	"context"
	"fmt"
	"log"

	"github.com/redis/go-redis/v9"
)

var (
	RedisClient *redis.Client
	Ctx         = context.Background()
)

// ConnectRedis initializes a Redis client
func ConnectRedis() error {
	RedisClient = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379", // Default Redis address
		Password: "",               // No password (unless set in Redis config)
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
