# List of venue categories
categories = [
    "restaurant",
    "cafe",
    "bar",
    "park",
    "museum",
    "theater",
    "cinema",
    "library",
    "shopping mall",
    "amusement park",
    "zoo",
    "aquarium",
    "beach",
    "gym",
    "sports stadium",
    "concert hall",
    "art gallery",
    "nightclub",
    "spa",
    "hotel",
    "conference center",
]

# List of atmospheres/moods
atmospheres = [
    "relaxed",
    "chill",
    "lively",
    "romantic",
    "family-friendly",
    "adventurous",
    "quiet",
    "intimate",
    "luxurious",
    "casual",
    "formal",
    "trendy",
    "historic",
    "rustic",
    "modern",
]

# List of specific features/restrictions
features = [
    "no alcohol",
    "pet-friendly",
    "wheelchair accessible",
    "outdoor seating",
    "vegan options",
    "gluten-free options",
    "live music",
    "free Wi-Fi",
    "kid-friendly",
    "parking available",
    "scenic views",
    "24-hour service",
    "reservations required",
    "happy hour",
    "delivery available",
]

# Function to get descriptors as a dictionary
def get_descriptors():
    return {
        "categories": categories,
        "atmospheres": atmospheres,
        "features": features,
    }
