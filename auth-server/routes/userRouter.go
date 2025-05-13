package routes

import (
	"github.com/akgupta-47/auth-module/controller"
	"github.com/akgupta-47/auth-module/middleware"
	"github.com/gofiber/fiber/v2"
)

func UserRoutes(app *fiber.App) {
	app.Use(middleware.Authenticate)
	app.Get("/users", controller.GetUsers)
	app.Get("/users/:user_id", controller.GetUser)
	app.Get("/users/test", controller.TestRoute)
}
