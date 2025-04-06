package router

import (
	"github.com/akgupta-47/go-service/controller"
	"github.com/gofiber/fiber/v2"
)

func OrderRoutes(app *fiber.App) {
	// orders := api.Group("/orders", AuthMiddleware) (adding midleware)
	orderRoutes := app.Group("/orders")
	orderRoutes.Get("/user", controller.GetOrdersUser)
	orderRoutes.Get("/shop/:shop_id", controller.GetOrdersShop)
	orderRoutes.Get("/:order_id", controller.GetOrderById)
	orderRoutes.Post("/user", controller.CreateOrder)
}
