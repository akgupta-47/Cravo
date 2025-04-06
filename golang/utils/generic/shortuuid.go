package utils

import (
	"database/sql/driver"
	"errors"

	"github.com/lithammer/shortuuid/v4"
)

// ShortUUID type (acts like uuid.UUID but shorter)
type ShortUUID string

// New generates a new ShortUUID
func NewShortUUID() ShortUUID {
	return ShortUUID(shortuuid.New())
}

// Scan converts database value to ShortUUID (implements sql.Scanner)
func (s *ShortUUID) Scan(value interface{}) error {
	str, ok := value.(string)
	if !ok {
		return errors.New("invalid ShortUUID format")
	}
	*s = ShortUUID(str)
	return nil
}

// Value converts ShortUUID to database format (implements driver.Valuer)
func (s ShortUUID) Value() (driver.Value, error) {
	return string(s), nil
}

// String converts ShortUUID to string
func (s ShortUUID) String() string {
	return string(s)
}
