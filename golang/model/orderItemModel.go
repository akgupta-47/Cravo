package models

import (
	"time"

	utils "github.com/akgupta-47/go-service/utils/generic"
	"gorm.io/gorm"
)

// OrderItem Model (Composite Primary Key: OrderID + ProductID)
type OrderItem struct {
	OrderID   *utils.ShortUUID `gorm:"type:varchar(22);not null;primaryKey" json:"order_id"`
	ProductID utils.ShortUUID  `gorm:"type:varchar(22);not null;primaryKey" json:"product_id" validate:"required"`
	Quantity  int32            `gorm:"not null;check:quantity > 0" json:"quantity" validate:"required,gt=0"`
	Available bool             `gorm:"default:false" json:"available"`
	CreatedAt time.Time        `gorm:"default:now()" json:"created_at"`
}

// BeforeCreate Hook to Ensure OrderID & ProductID Are Set
func (oi *OrderItem) BeforeCreate(tx *gorm.DB) error {
	if oi.OrderID == nil || oi.ProductID == "" {
		return gorm.ErrMissingWhereClause // Prevent saving if OrderID or ProductID is empty
	}
	return nil
}
