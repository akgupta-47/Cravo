package services

import (
	"context"
	"time"

	database "github.com/akgupta-47/auth-module/db"
	"github.com/akgupta-47/auth-module/helpers"
	models "github.com/akgupta-47/auth-module/models"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

// var profileCollection = database.CravoDB.Collection("profile")

func FetchUserProfiles(c *fiber.Ctx, userID primitive.ObjectID) ([]*models.Profile, error) {
	var profiles []*models.Profile
	query := bson.M{"user_id": userID}

	cursor, err := database.CravoDB.Collection("profile").Find(c.Context(), query)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(c.Context())

	if err = cursor.All(c.Context(), &profiles); err != nil {
		return nil, err
	}

	if len(profiles) == 0 {
		return nil, mongo.ErrNoDocuments
	}	

	return profiles, nil
}

func CreateNewProfile(c *fiber.Ctx, tempProfile *models.Profile) (primitive.ObjectID, error) {
	tempProfile.IsComplete = helpers.IsProfileComplete(tempProfile)
	
	var expiresAt *time.Time
	if !tempProfile.IsComplete {
		expiry := time.Now().Add(2 * time.Hour)
		expiresAt = &expiry
		tempProfile.ExpiresAt = expiresAt
	}

	if (database.CravoDB.Collection("profile") == nil) {
		return primitive.NilObjectID, c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "profile collection not found",
		})
	}

	// fmt.Printf("%+v\n", yourStruct) // Shows field names and values

	result, err := database.CravoDB.Collection("profile").InsertOne(c.Context(), tempProfile)
	if err != nil {
		return primitive.NilObjectID, 
		c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
	}

	insertedId := result.InsertedID.(primitive.ObjectID)

    return insertedId, nil
}

func UpdateUserProfile(c *fiber.Ctx, updateData *models.Profile, profileID primitive.ObjectID) (error) {
	
	updateDoc := helpers.BuildUpdateDocument(&updateData)
	if len(updateDoc["$set"].(bson.M)) == 0 {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "No fields to update"})
	}

	if (database.CravoDB.Collection("profile") == nil) {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "profile collection not found",
		})
	}

	// Always update `updated_at`
	updateDoc["$set"].(bson.M)["updated_at"] = time.Now()

	filter := bson.M{"_id": profileID}
	result, err := database.CravoDB.Collection("profile").UpdateOne(context.TODO(), filter, updateDoc)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Update failed"})
	}

	if result.MatchedCount == 0 {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Profile not found"})
	}

	return nil
}