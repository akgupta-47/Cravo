package helpers

import (
	"math"

	"github.com/akgupta-47/auth-module/models"
	"go.mongodb.org/mongo-driver/bson/primitive"
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
           p.UserID != nil && *p.UserID != primitive.NilObjectID &&
           IsSet(p.Name) &&
           IsSet(p.HouseNumber) &&
           IsSet(p.Street) &&
           IsSet(p.PhoneNumber) &&
           IsSet(p.City) &&
           IsSet(p.Pincode) &&
           p.LoggedIn &&
           p.IsActive &&
           p.Latitude != 0 &&
           p.Longitude != 0
}

func GetBestAddress(addresses []*models.Profile, lat, lon float64, matchRadius float64) *models.Profile {
	var (
		completeProfiles   []models.AddressWithDistance
		incompleteProfiles []models.AddressWithDistance
	)

	for _, addr := range addresses {
		distance := HaversineDistance(lat, lon, addr.Latitude, addr.Longitude)
		if distance <= matchRadius {
			entry := models.AddressWithDistance{Profile: addr, Distance: distance}
			if addr.IsComplete {
				completeProfiles = append(completeProfiles, entry)
			} else {
				incompleteProfiles = append(incompleteProfiles, entry)
			}
		}
	}

	// Function to find the address with the least distance
	findClosest := func(profiles []models.AddressWithDistance) *models.Profile {
		if len(profiles) == 0 {
			return nil
		}
		min := profiles[0]
		for _, p := range profiles[1:] {
			if p.Distance < min.Distance {
				min = p
			}
		}
		return min.Profile
	}

    if best := findClosest(completeProfiles); best != nil {
		return best
	}
	if best := findClosest(incompleteProfiles); best != nil {
		return best
	}

    // no profile found
    return nil
}