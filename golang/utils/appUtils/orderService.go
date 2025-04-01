package helper

import (
	models "github.com/akgupta-47/go-service/model"
	"github.com/go-playground/validator/v10"
)

// Validator instance
var validate = validator.New()

func validationMsg(tag string, fieldName string, param string) string {
	// Custom messages based on failed validation rule
	switch tag {
	case "required":
		return fieldName + " is required"
	case "gt":
		return fieldName + " must be greater than " + param
	case "uuid4":
		return fieldName + " must be a valid UUID"
	case "email":
		return fieldName + " must be a valid email address"
	default:
		return "Invalid " + fieldName
	}
}

func ValidateOrder(order models.Order) map[string]string {
	// Step 1: Validate Order Struct
	if err := validate.Struct(order); err != nil {
		errors := extractValidationErrors(err)
		return errors
	}

	// Step 2: Validate Each OrderItem in the Items Slice
	for i, item := range order.Items {
		if err := validate.Struct(item); err != nil {
			errors := extractValidationErrors(err)

			// Include index to indicate which order item has validation errors
			for key, val := range errors {
				errors[key] = val + " (OrderItem[" + string(i) + "])"
			}

			return errors
		}
	}

	return nil
}

// Helper Function: Extracts Validation Errors
func extractValidationErrors(err error) map[string]string {
	errors := make(map[string]string)
	for _, err := range err.(validator.ValidationErrors) {
		errors[err.Field()] = validationMsg(err.Tag(), err.Field(), err.Param())
	}
	return errors
}
