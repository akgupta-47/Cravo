package controller

import (
	"context"
	"encoding/json"
	"os"
	"strings"
	"time"

	database "github.com/akgupta-47/auth-module/db"
	models "github.com/akgupta-47/auth-module/models"
	jwt "github.com/dgrijalva/jwt-go"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
)

var SECRET_KEY string = os.Getenv("SECRET_KEY")

var (
	googleOauthConfig = &oauth2.Config{
		RedirectURL:  "http://localhost:3000/auth/google/callback",
		ClientID:     "YOUR_GOOGLE_CLIENT_ID",
		ClientSecret: "YOUR_GOOGLE_CLIENT_SECRET",
		Scopes:       []string{"https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"},
		Endpoint:     google.Endpoint,
	}
	jwtSecret = []byte(SECRET_KEY)
)

func HandleGoogleLogin(c *fiber.Ctx) error {
	url := googleOauthConfig.AuthCodeURL("state-token", oauth2.AccessTypeOffline)
	return c.Redirect(url, fiber.StatusTemporaryRedirect)
}

func HandleGoogleCallback(c *fiber.Ctx) error {
	code := c.Query("code")
	if code == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Missing code param"})
	}

	token, err := googleOauthConfig.Exchange(context.Background(), code)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Token exchange failed"})
	}

	client := googleOauthConfig.Client(context.Background(), token)
	resp, err := client.Get("https://www.googleapis.com/oauth2/v2/userinfo")
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to fetch user info"})
	}
	defer resp.Body.Close()

	var user struct {
		Email string `json:"email"`
		Name  string `json:"name"`
		Id    string `json:"id"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&user); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Decode error"})
	}

	// Create JWT token
	claims := jwt.MapClaims{
		"email":     user.Email,
		"name":      user.Name,
		"sub":       user.Id,
		"loginType": "google",
		"exp":       time.Now().Add(time.Hour * 24).Unix(),
	}

	jwtToken := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	signedToken, err := jwtToken.SignedString(jwtSecret)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to sign token"})
	}

	// Return token (or set cookie here)
	return c.JSON(fiber.Map{"token": signedToken})
}

func HandleSignup(c *fiber.Ctx) error {
    code := c.Query("code")
    if code == "" {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Missing code param"})
    }

    token, err := googleOauthConfig.Exchange(context.Background(), code)
    if err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Token exchange failed"})
    }

    client := googleOauthConfig.Client(context.Background(), token)
    resp, err := client.Get("https://www.googleapis.com/oauth2/v2/userinfo")
    if err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to fetch user info"})
    }
    defer resp.Body.Close()

    var user struct {
        Email string `json:"email"`
        Name  string `json:"name"`
        Id    string `json:"id"`
    }

    if err := json.NewDecoder(resp.Body).Decode(&user); err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Decode error"})
    }

    // Check if user already exists in the database
    userCollection := database.GetUserCollection()
    var existingUser bson.M
    err = userCollection.FindOne(context.Background(), bson.M{"email": user.Email}).Decode(&existingUser)
    if err == nil {
        return c.Status(fiber.StatusConflict).JSON(fiber.Map{"error": "User already exists"})
    } else if err != mongo.ErrNoDocuments {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Database error"})
    }

	newUser := new(models.User)
	newUser.Email = &user.Email
	newUser.First_name = &strings.Split(user.Name, " ")[0]
	newUser.Last_name = &strings.Split(user.Name, " ")[1]
	newUser.GoogleID = &user.Id
	newUser.Created_at = time.Now()
	newUser.Updated_at = time.Now()

    _, err = userCollection.InsertOne(context.Background(), newUser)
    if err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to create user"})
    }

    // Create JWT token
    claims := jwt.MapClaims{
        "email":     user.Email,
        "name":      user.Name,
        "sub":       user.Id,
        "loginType": "google",
        "exp":       time.Now().Add(time.Hour * 24).Unix(),
    }

    jwtToken := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    signedToken, err := jwtToken.SignedString(jwtSecret)
    if err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to sign token"})
    }

    // Return token
    return c.JSON(fiber.Map{"message": "User signed up successfully", "token": signedToken})
}