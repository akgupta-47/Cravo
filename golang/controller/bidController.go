package controller

import (
	models "github.com/akgupta-47/go-service/model"
	helper "github.com/akgupta-47/go-service/utils/appUtils"
	utils "github.com/akgupta-47/go-service/utils/generic"
	"github.com/gofiber/fiber/v2"
)

func PlaceBid(c *fiber.Ctx) error {
	var bid models.Bid

	// Parse JSON request
	if err := c.BodyParser(&bid); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request body"})
	}

	// Store bid and publish event
	if err := helper.StoreBidAndPublish(bid); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(fiber.Map{"message": "Bid placed successfully"})
}

func AcceptBid(c *fiber.Ctx) error {
	var bidId utils.ShortUUID

	if err := c.BodyParser(bidId); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request body"})
	}

	if err := helper.AcceptOrder(bidId); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return nil
}
