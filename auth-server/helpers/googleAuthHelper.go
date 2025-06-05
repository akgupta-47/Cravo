package helpers

import (
	"encoding/base64"
	"encoding/json"
	"errors"
	"net/http"
	"net/url"
	"os"
	"strings"
)

type GoogleTokenResponse struct {
    AccessToken string `json:"access_token"`
    ExpiresIn   int    `json:"expires_in"`
    IdToken     string `json:"id_token"`
    Scope       string `json:"scope"`
    TokenType   string `json:"token_type"`
}

func exchangeCodeForToken(code string) (*GoogleTokenResponse, error) {
    values := url.Values{}
    values.Set("client_id", os.Getenv("GOOGLE_CLIENT_ID"))
    values.Set("client_secret", os.Getenv("GOOGLE_CLIENT_SECRET"))
    values.Set("code", code)
    values.Set("grant_type", "authorization_code")
    values.Set("redirect_uri", os.Getenv("GOOGLE_REDIRECT_URI"))

    resp, err := http.PostForm("https://oauth2.googleapis.com/token", values)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    var tokenRes GoogleTokenResponse
    if err := json.NewDecoder(resp.Body).Decode(&tokenRes); err != nil {
        return nil, err
    }

    return &tokenRes, nil
}

type GoogleIDTokenPayload struct {
    Sub           string `json:"sub"`          // Google user ID
    Email         string `json:"email"`
    EmailVerified bool   `json:"email_verified"`
    Name          string `json:"name"`
    Picture       string `json:"picture"`
    GivenName     string `json:"given_name"`
    FamilyName    string `json:"family_name"`
    Locale        string `json:"locale"`
}

func decodeIDToken(idToken string) (*GoogleIDTokenPayload, error) {
    parts := strings.Split(idToken, ".")
    if len(parts) < 2 {
        return nil, errors.New("invalid JWT")
    }

    payload, err := base64.RawURLEncoding.DecodeString(parts[1])
    if err != nil {
        return nil, err
    }

    var userInfo GoogleIDTokenPayload
    if err := json.Unmarshal(payload, &userInfo); err != nil {
        return nil, err
    }

    return &userInfo, nil
}
