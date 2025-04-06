package models

import (
	"time"

	utils "github.com/akgupta-47/go-service/utils/generic"
	"gorm.io/gorm"
)

// Order represents an order in a PostgreSQL database
type Order struct {
	ID         utils.ShortUUID  `gorm:"type:varchar(22);primaryKey" json:"id"`
	Total      float64          `gorm:"not null;check:total > 0" json:"total" validate:"required,gt=0"`
	UserID     *string          `gorm:"type:varchar(255);not null" json:"user_id"`
	TrackID    *utils.ShortUUID `gorm:"type:varchar(22)" json:"track_id,omitempty" validate:"omitempty"`
	ShopID     string           `gorm:"type:varchar(255);not null" json:"shop_id" validate:"required"`
	ProfileID  string           `gorm:"type:varchar(255);not null" json:"profile_id" validate:"required"`
	PaymentID  utils.ShortUUID  `gorm:"type:varchar(22);not null;unique" json:"payment_id" validate:"required"`
	BidID      *string          `gorm:"type:varchar(255)" json:"bid_id,omitempty" validate:"omitempty"`
	FeedbackID *utils.ShortUUID `gorm:"type:varchar(22)" json:"feedback_id,omitempty" validate:"omitempty"`
	CreatedAt  time.Time        `gorm:"default:now()" json:"created_at"`
	UpdatedAt  time.Time        `gorm:"default:now()" json:"updated_at"`
	Items      []OrderItem      `gorm:"foreignKey:OrderID;constraint:OnDelete:CASCADE" json:"items"`
}

// BeforeCreate Hook to Ensure ID is Set
func (o *Order) BeforeCreate(tx *gorm.DB) error {
	if o.ID == "" {
		o.ID = utils.NewShortUUID()
	}
	return nil
}
