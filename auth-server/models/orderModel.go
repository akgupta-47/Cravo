package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// Order represents an order in a PostgreSQL database
type Order struct {
	ID         uuid.UUID      `gorm:"type:uuid;default:gen_random_uuid();primaryKey" json:"id"`
	Total      float64        `gorm:"not null;check:total > 0" json:"total" validate:"required,gt=0"`
	UserID     uuid.UUID      `gorm:"type:uuid;not null" json:"user_id" validate:"required,uuid4"`
	TrackID    *string        `gorm:"type:varchar(255)" json:"track_id,omitempty" validate:"omitempty"`
	ShopID     uuid.UUID      `gorm:"type:uuid;not null" json:"shop_id" validate:"required,uuid4"`
	ProfileID  string         `gorm:"type:varchar(255);not null" json:"profile_id" validate:"required"`
	PaymentID  uuid.UUID      `gorm:"type:uuid;not null" json:"payment_id" validate:"required,uuid4"`
	BidID      *uuid.UUID     `gorm:"type:uuid" json:"bid_id,omitempty" validate:"omitempty,uuid4"`
	FeedbackID *string        `gorm:"type:varchar(100)" json:"feedback_id,omitempty" validate:"omitempty"`
	CreatedAt  time.Time      `gorm:"default:now()" json:"created_at"`
	UpdatedAt  time.Time      `gorm:"default:now()" json:"updated_at"`
	DeletedAt  gorm.DeletedAt `gorm:"index" json:"-"`
}
