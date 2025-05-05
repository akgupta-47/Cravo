package main

import (
	"log"
	"os"

	database "github.com/akgupta-47/auth-module/db"
	"github.com/akgupta-47/auth-module/producer"
	"github.com/gofiber/fiber/v2"

	"github.com/gofiber/fiber/v2/middleware/logger"

	"github.com/akgupta-47/auth-module/routes"
)

func main() {
	if err := database.ConnectDB(); err != nil {
		log.Fatal(err)
	}

	if err := database.ConnectSqlDB(); err != nil {
		log.Fatal(err)
	}

	// var userCollection = db.GetUserCollection()
	// fmt.Println(*userCollection)
	port := os.Getenv("PORT")

	if port == "" {
		port = "8000"
	}

	app := fiber.New()
	// Default middleware config
	app.Use(logger.New())
	app.Get("/api", func(c *fiber.Ctx) error {
		return c.SendString("I'm a GET request!")
	})

	routes.AuthRoutes(app)
	routes.UserRoutes(app)
	// routes.OrderRoutes(app)

	api := app.Group("/api/v1")
	api.Get("/all", producer.CreateComment)

	// routes.FRouter(app)
	log.Fatal(app.Listen(":" + port))
}
