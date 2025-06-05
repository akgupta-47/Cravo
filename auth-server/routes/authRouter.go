package routes

import (
	"github.com/akgupta-47/auth-module/controller"
	"github.com/gofiber/fiber/v2"
)

func AuthRoutes(app *fiber.App) {
	app.Post("users/signup", controller.Signup)
	app.Post("users/login", controller.Login)
	app.Get("/auth/google/login", controller.HandleGoogleLogin)
	app.Get("/auth/google/callback", controller.HandleGoogleCallback)
}
