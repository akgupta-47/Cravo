package services

import (
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

	result, err := database.CravoDB.Collection("profile").InsertOne(c.Context(), tempProfile)
	if err != nil {
		return primitive.NilObjectID, 
		c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
	}

	insertedId := result.InsertedID.(primitive.ObjectID)

    return insertedId, nil
}