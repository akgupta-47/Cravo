package controller

import (
	"time"

	"github.com/akgupta-47/auth-module/controller/services"
	helpers "github.com/akgupta-47/auth-module/helpers"
	models "github.com/akgupta-47/auth-module/models"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson/primitive"
)


func ComputeProfile(c *fiber.Ctx) error {
    const matchRadius = 150.0 // meters

	profileBody := new(models.Profile)

	if err := c.BodyParser(profileBody); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(models.ErrorJson{Error: err.Error()})
	}

	if (*profileBody.UserID != primitive.NilObjectID) {
		// 1. Fetch all user addresses
		addresses, err := services.FetchUserProfiles(c, *profileBody.UserID)
		if err != nil {
			return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
		}

		if bestAddress := helpers.GetBestAddress(addresses, profileBody.Latitude, profileBody.Longitude, matchRadius); bestAddress != nil {
			return c.Status(fiber.StatusOK).JSON(bestAddress)
		}		
	}

    // 3. No match found — check if there's a temp profile for this session
    // tempAddr, err := addressRepo.FindTemporaryByUser(userID)
    // if err == nil && tempAddr != nil {
    //     return tempAddr, nil // Reuse existing temp address
    // }

    // 4. Create a temporary profile
    newAddr := models.Profile{
        ID:        primitive.NewObjectID(),
        UserID:    profileBody.UserID,
        Latitude:  profileBody.Latitude,
        Longitude: profileBody.Longitude,
        Label:     "current_location",
        IsActive:  true,
		LoggedIn: false,
		IsComplete: false,
        CreatedAt: time.Now(),
        UpdatedAt: time.Now(),
    }
    if err := services.CreateNewProfile(c, &newAddr); err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
    }

    return c.Status(fiber.StatusOK).JSON(newAddr)
}

func GetAllUserProfiles(c *fiber.Ctx) error {

	userIDStr := c.Params("user_id")
	userID, err := primitive.ObjectIDFromHex(userIDStr)
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(models.ErrorJson{Error: err.Error()})
	}

	profiles, err := services.FetchUserProfiles(c, userID)
	if err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
    }

	return c.Status(fiber.StatusOK).JSON(profiles)
}

func CreateNewProfile(c *fiber.Ctx) error {

	newProfileBody := new(models.Profile)

	if err := c.BodyParser(newProfileBody); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(models.ErrorJson{Error: err.Error()})
	}

	if err := services.CreateNewProfile(c, newProfileBody); err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
    }

    return c.Status(fiber.StatusOK).JSON(newProfileBody)
}