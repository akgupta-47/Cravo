package controller

import (
	database "github.com/akgupta-47/go-service/db"
	models "github.com/akgupta-47/go-service/model"
	helper "github.com/akgupta-47/go-service/utils/appUtils"
	utils "github.com/akgupta-47/go-service/utils/generic"
	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func getLoggedInUser() string {
	return "1234"
}

func GetOrdersUser(c *fiber.Ctx) error {
	loggedin_user := getLoggedInUser()

	// userID := c.Locals("userID")
	if loggedin_user == "" {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Unauthorized"})
	}
	// if loggedin_user == nil {
	// 	return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Unauthorized"})
	// }
	// userUUID, err := uuid.Parse(userID.(string))
	// if err != nil {
	// 	return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid user ID"})
	// }

	var orders []models.Order

	if err := database.DB.Where("user_id = ?", loggedin_user).Find(&orders).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"message": "No orders found"})
		}
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to retrieve orders"})
	}

	// Return JSON response
	return c.JSON(orders)
}

func GetOrderById(c *fiber.Ctx) error {
	order_id := c.Params("order_id")

	if order_id == "" {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "order id not found"})
	}

	var order models.Order

	if err := database.DB.Where("id = ?", order_id).Find(&order).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"message": "No order found for " + order_id})
		}
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to retrieve order for " + order_id})
	}

	return c.JSON(order)
}

func GetOrdersShop(c *fiber.Ctx) error {
	shop_id := c.Params("shop_id")

	var orders []models.Order

	if err := database.DB.Where("shop_id = ?", shop_id).Find(&orders).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"message": "No orders found"})
		}
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to retrieve orders"})
	}

	// Return JSON response
	return c.JSON(orders)
}

// GetOrdersForShop fetches all orders for a given shop
func GetOrdersForShop(c *fiber.Ctx) error {
	// Extract shop ID from path parameters
	shopIDParam := c.Params("shop_id")

	if shopIDParam == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid shop ID"})
	}

	// Query orders for the given shop
	var orders []models.Order
	if err := database.DB.Where("shop_id = ?", shopIDParam).Find(&orders).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"message": "No orders found for this shop"})
		}
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to retrieve orders"})
	}

	// Return JSON response
	return c.JSON(orders)
}

// CreateOrder handles creating a new order
func CreateOrder(c *fiber.Ctx) error {
	// Parse request body into Order struct
	var order models.Order
	if err := c.BodyParser(&order); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request body"})
	}

	// Generate new UUID for Order ID (if not provided)
	if order.ID == "" {
		order.ID = utils.NewShortUUID()
	}
	loggedin_user := getLoggedInUser()
	order.UserID = &loggedin_user

	if validationErrors := helper.ValidateOrder(order); validationErrors != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": validationErrors})
	}

	tx := database.DB.Begin()

	// Insert Order into database
	if err := tx.Create(&order).Error; err != nil {
		tx.Rollback()
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to create order", "message": err.Error()})
	}

	// Insert Order Items
	for i := range order.Items {
		order.Items[i].OrderID = &order.ID
		if err := tx.Create(&order.Items[i]).Error; err != nil {
			tx.Rollback()
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to create order items", "message": err.Error()})
		}
	}

	// Commit transaction
	tx.Commit()

	// Return created order with items
	return c.Status(fiber.StatusCreated).JSON(fiber.Map{"message": "Order created successfully", "order": order})
}
