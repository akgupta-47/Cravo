package routes

import (
	"github.com/gofiber/fiber/v2"
)

func ProfileRoutes(app *fiber.App) {
	app.Post("profile/signup", nil)
}
