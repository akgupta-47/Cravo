package routes

import (
	"github.com/akgupta-47/auth-module/controller"
	"github.com/gofiber/fiber/v2"
)

func ProfileRoutes(app *fiber.App) {
	api := app.Group("/api/v1/profile")
	api.Post("/nearest", controller.ComputeProfile)
	api.Get("/user/:user_id", controller.GetAllUserProfiles)
	api.Post("/new", controller.CreateNewProfile)
	api.Put("/update/:profile_id", controller.UpdateProfile)
}
