package database

import (
	"fmt"
	"log"
	"os"

	models "github.com/akgupta-47/go-service/model"
	"github.com/joho/godotenv"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB // Global variable to store DB connection

// ConnectSqlDB initializes the PostgreSQL connection
func ConnectSqlDB() error {

	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal("Error loading .env file")
		return err
	}

	user := os.Getenv("POSTGRES_USER")
	password := os.Getenv("POSTGRES_PASSWORD")
	host := os.Getenv("POSTGRES_HOST")
	port := os.Getenv("POSTGRES_PORT")
	dbname := os.Getenv("POSTGRES_DB")
	sslmode := os.Getenv("SSL_MODE")

	// Define your database connection details
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=%s",
		host, user, password, dbname, port, sslmode)

	// Open connection using GORM
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})

	if err != nil {
		log.Fatalf("❌ Failed to connect to the database: %v", err)
		return err
	}

	db.AutoMigrate(&models.Order{})
	db.AutoMigrate(&models.OrderItem{})

	// Assign DB connection to global variable
	DB = db

	// Log success message
	fmt.Println("✅ Successfully connected to the PostgreSQL database")
	return nil
}
