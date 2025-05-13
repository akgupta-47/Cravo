package helpers

import (
	"reflect"

	"go.mongodb.org/mongo-driver/bson"
)

func IsSet(s *string) bool {
    return s != nil && *s != ""
}

// Utility to build a BSON $set from a struct with non-nil fields
func BuildUpdateDocument(updateData interface{}) bson.M {
	v := reflect.ValueOf(updateData)
	// Handle nil
	if !v.IsValid() || v.IsNil() {
		return bson.M{} // or return an error if appropriate
	}

	// Handle pointer-to-pointer
	for v.Kind() == reflect.Ptr {
		v = v.Elem()
	}

	// Make sure we now have a struct
	if v.Kind() != reflect.Struct {
		return bson.M{} // or return an error
	}
	
	t := v.Type()

	set := bson.M{}
	for i := 0; i < v.NumField(); i++ {
		fieldValue := v.Field(i)
		fieldType := t.Field(i)

		// Skip ID field
		if fieldType.Name == "ID" {
			continue
		}

		// Skip nil pointers
		if fieldValue.Kind() == reflect.Ptr && fieldValue.IsNil() {
			continue
		}

		// Get bson tag (fallback to field name)
		bsonTag := fieldType.Tag.Get("bson")
		if bsonTag == "" || bsonTag == "-" {
			continue
		}
		bsonKey := bsonTag
		if commaIdx := indexComma(bsonKey); commaIdx != -1 {
			bsonKey = bsonKey[:commaIdx]
		}

		set[bsonKey] = fieldValue.Interface()
	}

	return bson.M{"$set": set}
}

// Helper: get index of first comma in a tag
func indexComma(s string) int {
	for i, ch := range s {
		if ch == ',' {
			return i
		}
	}
	return -1
}
