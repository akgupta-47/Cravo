package controller

import (
	"fmt"
	"log"

	database "github.com/akgupta-47/go-service/db"
	"github.com/gofiber/websocket/v2"
)

// WebSocketHandler upgrades HTTP to WebSocket
func WebSocketHandler(c *websocket.Conn) {
	fmt.Println("New WebSocket connection")

	// Subscribe to Redis bids channel
	pubsub := database.RedisClient.Subscribe(database.Ctx, "bids_channel")
	defer pubsub.Close()

	ch := pubsub.Channel() // Get message channel

	// Listen for bid updates
	for msg := range ch {
		err := c.WriteMessage(websocket.TextMessage, []byte(msg.Payload))
		if err != nil {
			log.Println("Error sending WebSocket message:", err)
			break
		}
	}
}
