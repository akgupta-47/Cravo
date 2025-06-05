package controller

import (
	"fmt"
	"log"
	"strconv"
	"time"

	database "github.com/akgupta-47/auth-module/db"
	"github.com/akgupta-47/auth-module/helpers"
	"github.com/akgupta-47/auth-module/models"
	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"golang.org/x/crypto/bcrypt"
)

// var userCollection = db.Mgi.Db.Collection("user")
var validate = validator.New()

// @Router = /test
// @HttpMethod = GET
// @Description = Test route to print user type from headers.
// @param = None
// @Return = JSON response with status OK.
// @ErrorCodes = None
func TestRoute(c *fiber.Ctx) error {
	utype := c.Get("user_type")
	fmt.Println(utype)
	return c.Status(fiber.StatusOK).JSON(fiber.Map{})
}

// @Router = None
// @HttpMethod = None
// @Description = Hashes a password using bcrypt.
// @param = [password, string, the password to hash]
// @Return = [hashed_password, string, the hashed password]
// @ErrorCodes = None
func HashPassword(password string) string {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	if err != nil {
		log.Panic(err)
	}
	return string(bytes)
}

// @Router = None
// @HttpMethod = None
// @Description = Verifies a password against a hashed password.
// @param = [userPassword, string, the hashed password], [providedPassword, string, the plain text password]
// @Return = [isValid, bool, whether the password is valid], [message, string, error message if invalid]
// @ErrorCodes = None
func VerifyPassword(userPassword string, providedPassword string) (bool, string) {
	err := bcrypt.CompareHashAndPassword([]byte(providedPassword), []byte(userPassword))
	check := true
	msg := ""

	if err != nil {
		msg = "email or password incorrect!!"
		check = false
	}
	return check, msg
}

// @Router = /signup
// @HttpMethod = POST
// @Description = Creates a new user in the database.
// @param = [user_object, model, fields required to create a new user]
// @Return = JSON response with the inserted user ID.
// @ErrorCodes = 
// - 400: Bad Request if validation fails or body parsing fails.
// - 500: Internal Server Error if database insertion fails or email already exists.
func Signup(c *fiber.Ctx) error {
	var userCollection = database.GetUserCollection()
	user := new(models.User)

	if err := c.BodyParser(user); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(models.ErrorJson{Error: err.Error()})
	}

	validationErr := validate.Struct(user)
	if validationErr != nil {
		return c.Status(fiber.StatusBadRequest).JSON(models.ErrorJson{Error: validationErr.Error()})
	}

	// count, err := userCollection.CountDocuments(c.Context(), bson.M{"email": user.Email})

	count, err := userCollection.CountDocuments(c.Context(), bson.M{"email": user.Email})
	if err != nil {
		log.Panic(err)
		return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: "Error while counting the documents!!"})
	}
	// fmt.Println(count)
	if count > 0 {
		return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: "Email already exists!!"})
	}
	// return nil
	password := HashPassword(*user.Password)
	user.Password = &password

	user.Created_at, _ = time.Parse(time.RFC3339, time.Now().Format(time.RFC3339))
	user.Updated_at, _ = time.Parse(time.RFC3339, time.Now().Format(time.RFC3339))
	user.ID = primitive.NewObjectID()
	user.User_id = user.ID.Hex()
	token, refreshToken, _ := helpers.GenerateAllTokens(*user.Email, *user.First_name, *user.Last_name, *user.User_type, user.User_id)
	user.Token = &token
	user.Refresh_token = &refreshToken

	resultInsertionNumber, insertionErr := userCollection.InsertOne(c.Context(), user)
	if insertionErr != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: "User Item was not created!!"})
	}
	return c.Status(fiber.StatusOK).JSON(resultInsertionNumber)
}

// @Router = /login
// @HttpMethod = POST
// @Description = Authenticates a user and generates tokens.
// @param = [user_object, model, email and password required for login]
// @Return = JSON response with user details and tokens.
// @ErrorCodes = 
// - 400: Bad Request if body parsing fails.
// - 500: Internal Server Error if email or password is incorrect or user not found.
func Login(c *fiber.Ctx) error {
	var userCollection = database.GetUserCollection()
	user := new(models.User)
	foundUser := new(models.User)

	// while testing check what happens if empty email is sent
	if err := c.BodyParser(user); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(models.ErrorJson{Error: err.Error()})
	}

	err := userCollection.FindOne(c.Context(), bson.M{"email": user.Email}).Decode(&foundUser)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: "email or password incorrect"})
	}

	passwordIsValid, msg := VerifyPassword(*user.Password, *foundUser.Password)
	if !passwordIsValid {
		return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: msg})
	}

	if foundUser.Email == nil {
		return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: "user not found!!"})
	}
	token, refreshToken, _ := helpers.GenerateAllTokens(*foundUser.Email, *foundUser.First_name, *foundUser.Last_name, *foundUser.User_type, foundUser.User_id)
	helpers.UpdateAllTokens(c, token, refreshToken, foundUser.User_id)

	err = userCollection.FindOne(c.Context(), bson.M{"user_id": foundUser.User_id}).Decode(&foundUser)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
	}

	cookie := fiber.Cookie{
		Name:     "auth",
		Value:    token,
		HTTPOnly: true,
	}

	c.Cookie(&cookie)

	return c.Status(fiber.StatusOK).JSON(foundUser)
}

// @Router = /users
// @HttpMethod = GET
// @Description = Retrieves a paginated list of users.
// @param = 
// - [recordPerPage, query, optional, number of records per page (default: 10)]
// - [page, query, optional, page number (default: 1)]
// @Return = JSON response with paginated user data and total count.
// @ErrorCodes = 
// - 400: Bad Request if user type is not ADMIN.
// - 500: Internal Server Error if database query fails.
func GetUsers(c *fiber.Ctx) error {
	var userCollection = database.GetUserCollection()
	if err := helpers.CheckUserType(c, "ADMIN"); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(models.ErrorJson{Error: err.Error()})
	}

	recordsPerPage, err := strconv.Atoi(c.Query("recordPerPage"))
	if err != nil || recordsPerPage < 1 {
		recordsPerPage = 10
	}

	page, err := strconv.Atoi(c.Query("page"))
	if err != nil || page < 1 {
		page = 1
	}

	startIndex := (page - 1) * recordsPerPage
	startIndex, err = strconv.Atoi(c.Query("startIndex"))

	matchStage := bson.D{
		{Key: "$match", Value: bson.D{}},
	}
	
	groupStage := bson.D{
		{Key: "$group", Value: bson.D{
			{Key: "_id", Value: bson.D{{Key: "_id", Value: "null"}}},
			{Key: "total_count", Value: bson.D{{Key: "$sum", Value: 1}}},
			{Key: "data", Value: bson.D{{Key: "$push", Value: "$$ROOT"}}},
		}},
	}
	
	projectStage := bson.D{
		{Key: "$project", Value: bson.D{
			{Key: "_id", Value: 0},
			{Key: "total_count", Value: 1},
			{Key: "user_items", Value: bson.D{
				{Key: "$slice", Value: []interface{}{"$data", startIndex, recordsPerPage}},
			}},
		}},
	}
	

	result, err := userCollection.Aggregate(c.Context(), mongo.Pipeline{matchStage, groupStage, projectStage})

	if err != nil {
		c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: "error while listing user items"})
	}

	var allusers []bson.M
	if err = result.All(c.Context(), &allusers); err != nil {
		log.Fatal(err)
	}

	return c.Status(fiber.StatusOK).JSON(allusers[0])
}

// @Router = /users/{user_id}
// @HttpMethod = GET
// @Description = Retrieves a user by their user ID.
// @param = [user_id, path, required, the ID of the user to retrieve]
// @Return = JSON response with user data.
// @ErrorCodes = 
// - 400: Bad Request if user type does not match the user ID.
// - 500: Internal Server Error if database query fails.
func GetUser(c *fiber.Ctx) error {
	var userCollection = database.GetUserCollection()
	userId := c.Params("user_id")

	if err := helpers.MatchUserTypeToUid(c, userId); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(models.ErrorJson{Error: err.Error()})
	}

	var user models.User
	query := bson.M{"user_id": userId}
	err := userCollection.FindOne(c.Context(), query).Decode(&user)

	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(models.ErrorJson{Error: err.Error()})
	}

	return c.Status(fiber.StatusOK).JSON(user)
}
