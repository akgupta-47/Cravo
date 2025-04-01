package helper

import (
	"encoding/json"
	"fmt"

	database "github.com/akgupta-47/go-service/db"
	models "github.com/akgupta-47/go-service/model"
	utils "github.com/akgupta-47/go-service/utils/generic"
)

// StoreBidAndPublish stores a bid in Redis and publishes a real-time update
func StoreBidAndPublish(bid models.Bid) error {
	if bid.ID == "" {
		bid.ID = utils.NewShortUUID()
	}

	// Convert bid to JSON
	bidJSON, err := json.Marshal(bid)
	if err != nil {
		return fmt.Errorf("failed to marshal bid: %w", err)
	}

	// Store bid in Redis temporarily
	key := fmt.Sprintf("bids:%s", bid.ID)
	err = database.RedisClient.RPush(database.Ctx, key, bidJSON).Err()
	if err != nil {
		return fmt.Errorf("failed to store bid in Redis: %w", err)
	}

	// Publish the bid event to Redis Pub/Sub
	err = database.RedisClient.Publish(database.Ctx, "bids_channel", bidJSON).Err()
	if err != nil {
		return fmt.Errorf("failed to publish bid event: %w", err)
	}

	fmt.Println("Bid stored and published to Redis Pub/Sub")
	return nil
}

// MoveBidsToPostgres transfers bids from Redis to PostgreSQL
func MoveBidsToPostgres(orderID utils.ShortUUID) error {
	key := fmt.Sprintf("bids:%s", orderID)

	// Retrieve all bids from Redis
	bids, err := database.RedisClient.LRange(database.Ctx, key, 0, -1).Result()
	if err != nil {
		return fmt.Errorf("failed to retrieve bids from Redis: %w", err)
	}

	if len(bids) == 0 {
		fmt.Println("No bids found in Redis for this order.")
		return nil
	}

	// Start transaction for inserting bids into PostgreSQL
	tx := database.DB.Begin()

	// Loop through bids and insert into PostgreSQL
	for _, bidJSON := range bids {
		var bid models.Bid
		if err := json.Unmarshal([]byte(bidJSON), &bid); err != nil {
			tx.Rollback()
			return fmt.Errorf("failed to unmarshal bid JSON: %w", err)
		}

		// Insert bid into PostgreSQL
		if err := tx.Create(&bid).Error; err != nil {
			tx.Rollback()
			return fmt.Errorf("failed to insert bid into PostgreSQL: %w", err)
		}
	}

	// Commit transaction
	tx.Commit()

	// Remove bids from Redis after storing in PostgreSQL
	database.RedisClient.Del(database.Ctx, key)
	fmt.Println("✅ Bids moved from Redis to PostgreSQL")
	return nil
}

func AcceptOrder(bidId utils.ShortUUID) error {

	return nil
}
