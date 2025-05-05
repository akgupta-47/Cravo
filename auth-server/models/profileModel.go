package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Profile struct {
    ID             primitive.ObjectID `bson:"_id,omitempty" json:"id"`
    UserID         primitive.ObjectID `bson:"user_id" json:"user_id"`
    Label          string             `bson:"label" json:"label"` // home, work, other
	Name          string             `bson:"name" json:"name"` // home, work, other
    HouseNumber    string             `bson:"house_number,omitempty" json:"house_number,omitempty"`
    Street         string             `bson:"street,omitempty" json:"street,omitempty"`
    Landmark       string             `bson:"landmark,omitempty" json:"landmark,omitempty"`
    Area           string             `bson:"area,omitempty" json:"area,omitempty"`
    City           string             `bson:"city" json:"city"`
    State          string             `bson:"state,omitempty" json:"state,omitempty"`
    Pincode        string             `bson:"pincode" json:"pincode"`
    Country        string             `bson:"country,omitempty" json:"country,omitempty"`
    Latitude       float64            `bson:"latitude" json:"latitude"`
    Longitude      float64            `bson:"longitude" json:"longitude"`
    IsDefault      bool               `bson:"is_default" json:"is_default"`
	IsComplete      bool               `bson:"is_complete" json:"is_complete"`
	LoggedIn       bool               `bson:"logged_id" json:"logged_id"`
    IsActive       bool               `bson:"is_active" json:"is_active"`
    PhoneNumber    string             `bson:"phone_number,omitempty" json:"phone_number,omitempty"`
    CreatedAt      time.Time          `bson:"created_at" json:"created_at"`
    UpdatedAt      time.Time          `bson:"updated_at" json:"updated_at"`
}
