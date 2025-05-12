package database

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type MongoInstance struct {
	Client *mongo.Client
	Db     *mongo.Database
}

const dbName = "auth-cravo"

var CravoDB *mongo.Database

var Mgi MongoInstance

// ConnectDB initializes the MongoDb connection
func ConnectDB() error {
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	mongoURI := os.Getenv("MONGODB_URL")

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
	if err != nil {
		log.Fatal(err)
	}

	CravoDB = client.Database(dbName)

	Mgi = MongoInstance{
		Client: client,
		Db:     CravoDB,
	}

	fmt.Println("Database Connected!!")
	return nil
}

// func createCollection(db *mongo.Database, collectionName string) error {
// 	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
// 	defer cancel()

// 	err := db.CreateCollection(ctx, collectionName)
// 	if err != nil {
// 		// If the collection already exists, you may want to handle it accordingly
// 		return err
// 	}
// 	return nil
// }

// func doesCollectionExist(db *mongo.Database, name string) (bool, error) {
// 	collections, err := db.ListCollectionNames(context.TODO(), bson.M{})
// 	if err != nil {
// 		return false, err
// 	}
// 	for _, coll := range collections {
// 		if coll == name {
// 			return true, nil
// 		}
// 	}
// 	return false, nil
// }


func GetUserCollection() *mongo.Collection {
	collection := Mgi.Db.Collection("user")
	return collection
}

// func GetProfileCollection(db *mongo.Database) *mongo.Collection {
// 	if db == nil {
// 		// log.Fatal("Database connection is not initialized")
		
// 		return nil
// 	}
// 	fmt.Println(Mgi)
// 	// Create collection if it doesn't exist
// 	collectionName := "profile"
// 	collectionExists, err := doesCollectionExist(db, collectionName)
// 	if err != nil {
// 		log.Fatalf("Error checking collection: %v", err)
// 	}

// 	if !collectionExists {
// 		if err := createCollection(db, collectionName); err != nil {
// 			log.Fatalf("Failed to create collection: %v", err)
// 		}
// 	}

// 	return db.Collection(collectionName)
// }

