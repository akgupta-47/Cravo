package utils

import (
	"errors"
	"os"

	jwt "github.com/dgrijalva/jwt-go"
)

var SECRET_KEY string = os.Getenv("SECRET_KEY")

type SignedDetails struct {
    Email      string `json:"email"`
    First_name string `json:"first_name"`
    Last_name  string `json:"last_name"`
    Uid        string `json:"uid"`
    User_type  string `json:"user_type"`
    jwt.StandardClaims
}

func ValidateToken(signedToken string) (*SignedDetails, error) {
    token, err := jwt.ParseWithClaims(
        signedToken,
        &SignedDetails{},
        func(token *jwt.Token) (interface{}, error) {
            return []byte(SECRET_KEY), nil // Or public key for RS256
        },
    )
    if err != nil {
        return nil, err
    }

    claims, ok := token.Claims.(*SignedDetails)
    if !ok || !token.Valid {
        return nil, errors.New("invalid token")
    }

    return claims, nil
}
