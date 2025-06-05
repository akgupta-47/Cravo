package database

import (
	"context"
	"fmt"
	"log"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func CreateIndexes(client *mongo.Client) error {
	// Define the database and collection
	collection := client.Database("yourDatabase").Collection("profiles")

	// List existing indexes
	existingIndexes, err := collection.Indexes().List(context.Background())
	if err != nil {
		return fmt.Errorf("could not list existing indexes: %v", err)
	}

	// Check if the desired index already exists
	var indexExists bool
	var expiryIndexExists bool
	for existingIndexes.Next(context.Background()) {
		var index bson.M
		if err := existingIndexes.Decode(&index); err != nil {
			log.Println("Failed to decode index:", err)
			continue
		}

		// Check for specific index name or fields to ensure it's not a duplicate
		if index["name"] == "user_id_1_is_default_1" {
			indexExists = true
		}

		if index["name"] == "expiresAt_1" {
			expiryIndexExists = true;
			return nil
		}
	}

	// Only create the user_id and is_default index if it doesn't exist
	if !indexExists {
		_, err := collection.Indexes().CreateOne(
			context.Background(),
			mongo.IndexModel{
				Keys: bson.D{
					{Key: "user_id", Value: 1},
					{Key: "is_default", Value: 1},
				},
				Options: options.Index().SetUnique(false),
			},
		)
		if err != nil {
			return fmt.Errorf("could not create user_id index: %v", err)
		}
		log.Println("User ID and Is Default Index created successfully.")
	}

	// Create TTL index on expiresAt (documents will automatically expire)
	if !expiryIndexExists {
		_, err = collection.Indexes().CreateOne(
		context.Background(),
		mongo.IndexModel{
			Keys: bson.D{
				{Key: "expiresAt", Value: 1}, // Sort ascending for TTL
			},
			Options: options.Index().SetExpireAfterSeconds(0), // Set expiration time to the value of expiresAt field
		},
		)
		if err != nil {
			return fmt.Errorf("could not create TTL index on expiresAt: %v", err)
		}
		log.Println("TTL index on expiresAt created successfully.")
	}

	return nil
}