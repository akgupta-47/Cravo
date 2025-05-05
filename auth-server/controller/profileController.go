package controller

import (
	"time"

	"github.com/akgupta-47/auth-module/controller/services"
	helpers "github.com/akgupta-47/auth-module/helpers"
	models "github.com/akgupta-47/auth-module/models"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson/primitive"
)


func ComputeProfile(c *fiber.Ctx, userID primitive.ObjectID, lat, lon float64) error {
    const matchRadius = 150.0 // meters

	if (userID != primitive.NilObjectID) {
		// 1. Fetch all user addresses
		addresses, err := services.FetchUserProfiles(c, userID)
		if err != nil {
			return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
		}
	
		// 2. Check if any address is within radius
		for _, addr := range addresses {
			distance := helpers.HaversineDistance(lat, lon, addr.Latitude, addr.Longitude)
			if distance <= matchRadius {
				return c.Status(fiber.StatusOK).JSON(addr)
			}
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
        UserID:    userID,
        Latitude:  lat,
        Longitude: lon,
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

func GetAllUserProfiles(c *fiber.Ctx, userID primitive.ObjectID) (error) {

	profiles, err := services.FetchUserProfiles(c, userID)
	if err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
    }

	return c.Status(fiber.StatusOK).JSON(profiles)
}
