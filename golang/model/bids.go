package models

import (
	"time"

	utils "github.com/akgupta-47/go-service/utils/generic"
	"gorm.io/gorm"
)

// Bid Model (Stored in PostgreSQL & Redis)
type Bid struct {
	ID           utils.ShortUUID  `gorm:"type:varchar(22);primaryKey" json:"id"`
	OrderID      *utils.ShortUUID `gorm:"type:varchar(22)" json:"order_id"`
	ShopID       string           `gorm:"type:varchar(12);not null;index" json:"shop_id"`
	ShopDistance float64          `gorm:"not null" json:"distance"`
	UserID       string           `gorm:"type:varchar(12);not null;index" json:"user_id"`
	Amount       float64          `gorm:"not null" json:"amount"`
	Status       string           `gorm:"not null;default:'Initiated'" json:"status"`
	CreatedAt    time.Time        `gorm:"default:now()" json:"created_at"`
}

func (b *Bid) BeforeCreate(tx *gorm.DB) (err error) {
	if b.ID == "" { // Ensure ID is not empty
		b.ID = utils.NewShortUUID() // Generate a new ShortUUID
	}
	return nil
}
