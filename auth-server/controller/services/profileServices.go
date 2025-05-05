package services

import (
	database "github.com/akgupta-47/auth-module/db"
	"github.com/akgupta-47/auth-module/helpers"
	models "github.com/akgupta-47/auth-module/models"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)


var profileCollection = database.GetProfileCollection()

func FetchUserProfiles(c *fiber.Ctx, userID primitive.ObjectID) ([]*models.Profile, error) {
	var profiles []*models.Profile
	query := bson.M{"user_id": userID}

	cursor, err := profileCollection.Find(c.Context(), query)
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

func CreateNewProfile(c *fiber.Ctx, tempProfile *models.Profile) (error) {

	tempProfile.IsComplete = helpers.IsProfileComplete(tempProfile)

	_, err := profileCollection.InsertOne(c.Context(), tempProfile)
	if err != nil {
		return err
	}

    return nil
}