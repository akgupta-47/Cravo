package helpers

import (
	"math"

	"github.com/akgupta-47/auth-module/models"
)

func HaversineDistance(lat1, lon1, lat2, lon2 float64) float64 {
	const R = 6371e3 // Earth radius in meters
	
	dLat := (lat2 - lat1) * math.Pi / 180
    dLon := (lon2 - lon1) * math.Pi / 180

    lat1Rad := lat1 * math.Pi / 180
    lat2Rad := lat2 * math.Pi / 180

    a := math.Sin(dLat/2)*math.Sin(dLat/2) +
         math.Cos(lat1Rad)*math.Cos(lat2Rad)*
         math.Sin(dLon/2)*math.Sin(dLon/2)

    c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))

    return R * c
}

func IsProfileComplete(p *models.Profile) bool {
    return p.Label != "" &&
           p.HouseNumber != "" &&
           p.Street != "" &&
           p.LoggedIn &&
           p.IsActive &&
           p.Latitude != 0 &&
           p.Longitude != 0 &&
           p.PhoneNumber != "" &&
           p.City != "" &&
           p.Pincode != "" &&
           p.Name != ""
}

