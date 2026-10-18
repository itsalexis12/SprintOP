from app.core.firebase import db

restaurants = [
    {
        "name": "La Abuela",
        "category": "Mexicana",
        "city": "Puebla",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1552566626-52f8b828add9",
        "avgRating": 4.5,
        "numRatings": 20,
    },
    {
        "name": "Pizza Central",
        "category": "Pizza",
        "city": "Puebla",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1513104890138-7c749659a591",
        "avgRating": 4.0,
        "numRatings": 12,
    },
]

for restaurant in restaurants:
    db.collection("restaurants").add(restaurant)

print("Datos semilla creados")