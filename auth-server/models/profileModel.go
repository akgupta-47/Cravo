package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Profile struct {
    ID             primitive.ObjectID `bson:"_id,omitempty" json:"id"`
    UserID         *primitive.ObjectID `bson:"user_id,omitempty" json:"user_id,omitempty"`
    Label          string             `bson:"label" json:"label"` // home, work, other
	Name           *string             `bson:"name,omitempty" json:"name,omitempty"` // home, work, other
    HouseNumber    *string             `bson:"house_number,omitempty" json:"house_number,omitempty"`
    Street         *string             `bson:"street,omitempty" json:"street,omitempty"`
    Landmark       *string             `bson:"landmark,omitempty" json:"landmark,omitempty"`
    Area           *string             `bson:"area,omitempty" json:"area,omitempty"`
    City           *string             `bson:"city,omitempty" json:"city,omitempty"`
    State          *string             `bson:"state,omitempty" json:"state,omitempty"`
    Pincode        *string             `bson:"pincode,omitempty" json:"pincode,omitempty"`
    Country        *string             `bson:"country,omitempty" json:"country,omitempty"`
    Latitude       float64            `bson:"latitude" json:"latitude"`
    Longitude      float64            `bson:"longitude" json:"longitude"`
    IsDefault      *bool               `bson:"is_default,omitempty" json:"is_default,omitempty"`
	IsComplete     bool               `bson:"is_complete" json:"is_complete"`
	LoggedIn       bool               `bson:"logged_in" json:"logged_in"`
    IsActive       bool               `bson:"is_active" json:"is_active"`
    PhoneNumber    *string             `bson:"phone_number,omitempty" json:"phone_number,omitempty"`
	ExpiresAt      *time.Time         `bson:"expiresAt,omitempty"`
    CreatedAt      time.Time          `bson:"created_at" json:"created_at,omitempty"`
    UpdatedAt      time.Time          `bson:"updated_at" json:"updated_at,omitempty"`
}

type AddressWithDistance struct {
	Profile  *Profile
	Distance float64
}
