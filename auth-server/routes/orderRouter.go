package routes

import (
	"github.com/akgupta-47/auth-gofib/controller"
	"github.com/gofiber/fiber/v2"
)

func OrderRoutes(app *fiber.App) {
	app.Post("/orders", controller.GetOrders)
}
