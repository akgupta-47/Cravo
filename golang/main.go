package main

import (
	"log"
	"os"

	"github.com/akgupta-47/go-service/controller"
	database "github.com/akgupta-47/go-service/db"
	router "github.com/akgupta-47/go-service/router"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/websocket/v2"
)

func main() {
	// if err := database.ConnectDB(); err != nil {
	// 	log.Fatal(err)
	// }

	if err := database.ConnectSqlDB(); err != nil {
		log.Fatal(err)
	}

	if err := database.ConnectRedis(); err != nil {
		log.Fatal(err)
	}

	// var userCollection = db.GetUserCollection()
	// fmt.Println(*userCollection)
	port := os.Getenv("PORT")

	if port == "" {
		port = "8080"
	}

	app := fiber.New()
	// Default middleware config
	app.Use(logger.New())

	app.Get("/ws/bids", websocket.New(controller.WebSocketHandler))
	app.Get("/api", func(c *fiber.Ctx) error {
		return c.SendString("I'm a GET request!")
	})

	// routes.AuthRoutes(app)
	// routes.UserRoutes(app)
	router.OrderRoutes(app)

	// api := app.Group("/api/v1")
	// api.Get("/all", producer.CreateComment)

	// routes.FRouter(app)
	log.Fatal(app.Listen(":" + port))
}
