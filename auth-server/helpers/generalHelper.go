package helpers

func IsSet(s *string) bool {
    return s != nil && *s != ""
}