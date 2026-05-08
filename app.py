import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Hardcoded Destination Database
DESTINATIONS = [
    {
        "city": "Tokyo",
        "country": "Japan",
        "vibes": ["Chaos", "Fashion", "Foodie"],
        "tagline": "Neon lights, high-tech subways, and world-class sushi.",
        "estimated_cost": "$2,200",
        "itinerary": [
            {"day": 1, "title": "Cyberpunk Vibes", "morning": "Shibuya Crossing breakfast", "afternoon": "Harajuku fashion crawl", "evening": "Golden Gai bar hopping"},
            {"day": 2, "title": "Tradition & Tech", "morning": "Senso-ji Temple", "afternoon": "Akihabara electric town", "evening": "Shinjuku skyline views"},
            {"day": 3, "title": "Foodie Heaven", "morning": "Tsukiji Outer Market", "afternoon": "TeamLab Borderless art", "evening": "Omakase dinner"}
        ]
    },
    {
        "city": "Kyoto",
        "country": "Japan",
        "vibes": ["History", "Spiritual", "Aloof"],
        "tagline": "Ancient temples, bamboo forests, and silent zen gardens.",
        "estimated_cost": "$1,800",
        "itinerary": [
            {"day": 1, "title": "The Golden Path", "morning": "Kinkaku-ji Temple", "afternoon": "Ryoan-ji Zen Garden", "evening": "Gion geisha district walk"},
            {"day": 2, "title": "Nature Whispers", "morning": "Arashiyama Bamboo Grove", "afternoon": "Tenryu-ji Temple", "evening": "Kaiseki traditional dinner"},
            {"day": 3, "title": "Spiritual Ascent", "morning": "Fushimi Inari Shrines", "afternoon": "Kiyomizu-dera Temple", "evening": "Pontocho Alley dinner"}
        ]
    },
    {
        "city": "Paris",
        "country": "France",
        "vibes": ["Fashion", "Romance", "Foodie"],
        "tagline": "The City of Light, pastries, and haute couture.",
        "estimated_cost": "$2,500",
        "itinerary": [
            {"day": 1, "title": "Iconic Paris", "morning": "Eiffel Tower sunrise", "afternoon": "Louvre Museum", "evening": "Seine River cruise"},
            {"day": 2, "title": "Chic Montmartre", "morning": "Sacre-Coeur Basilica", "afternoon": "Boulangerie crawl", "evening": "Moulin Rouge show"},
            {"day": 3, "title": "Haute Living", "morning": "Champs-Elysees shopping", "afternoon": "Tuileries Garden", "evening": "Michelin star dinner"}
        ]
    },
    {
        "city": "Marrakech",
        "country": "Morocco",
        "vibes": ["Chaos", "History", "Offbeat"],
        "tagline": "Spices, souks, and hidden riads in the Red City.",
        "estimated_cost": "$1,200",
        "itinerary": [
            {"day": 1, "title": "The Medina", "morning": "Jemaa el-Fnaa square", "afternoon": "Bahia Palace", "evening": "Traditional tagine in a riad"},
            {"day": 2, "title": "Hidden Gems", "morning": "Majorelle Garden", "afternoon": "Le Jardin Secret", "evening": "Rooftop terrace sunset"},
            {"day": 3, "title": "The Desert Edge", "morning": "Agafay desert trip", "afternoon": "Souk shopping", "evening": "Berber cultural performance"}
        ]
    },
    {
        "city": "Reykjavik",
        "country": "Iceland",
        "vibes": ["Nature", "Aloof", "Offbeat"],
        "tagline": "Volcanic landscapes, glaciers, and ethereal northern lights.",
        "estimated_cost": "$2,800",
        "itinerary": [
            {"day": 1, "title": "Fire & Ice", "morning": "Blue Lagoon soak", "afternoon": "South Coast waterfalls", "evening": "Northern Lights hunt"},
            {"day": 2, "title": "The Golden Circle", "morning": "Thingvellir Park", "afternoon": "Geysir geothermal area", "evening": "Gulfoss Waterfall"},
            {"day": 3, "title": "Coastal Vibes", "morning": "Reynisfjara Black Sand Beach", "afternoon": "Skogafoss hike", "evening": "Reykjavik harbor seafood"}
        ]
    },
    {
        "city": "New York",
        "country": "USA",
        "vibes": ["Chaos", "Fashion", "Foodie"],
        "tagline": "The concrete jungle where dreams are made of.",
        "estimated_cost": "$3,000",
        "itinerary": [
            {"day": 1, "title": "Manhattan Core", "morning": "Central Park walk", "afternoon": "Empire State Building", "evening": "Broadway show"},
            {"day": 2, "title": "Hip Brooklyn", "morning": "Brooklyn Bridge walk", "afternoon": "Williamsburg thrift shops", "evening": "Pizza crawl in DUMBO"},
            {"day": 3, "title": "Museum & Art", "morning": "The MET", "afternoon": "The High Line", "evening": "Chelsea Market dinner"}
        ]
    },
    {
        "city": "Varanasi",
        "country": "India",
        "vibes": ["Spiritual", "History", "Offbeat"],
        "tagline": "Life and death on the banks of the sacred Ganges.",
        "estimated_cost": "$800",
        "itinerary": [
            {"day": 1, "title": "Sacred Waters", "morning": "Ganges boat sunrise", "afternoon": "Walking the Ghats", "evening": "Ganga Aarti ceremony"},
            {"day": 2, "title": "Ancient Alleyways", "morning": "Kashi Vishwanath Temple", "afternoon": "Sarnath archaeological site", "evening": "Street food exploration"},
            {"day": 3, "title": "Spiritual Silence", "morning": "Yoga on the river", "afternoon": "Textile market visit", "evening": "Meditation at sunset"}
        ]
    },
    {
        "city": "Amalfi Coast",
        "country": "Italy",
        "vibes": ["Romance", "Nature", "Luxury"],
        "tagline": "Lemon groves, turquoise waters, and cliffside villas.",
        "estimated_cost": "$3,500",
        "itinerary": [
            {"day": 1, "title": "Positano Dream", "morning": "Beach time at Spiaggia Grande", "afternoon": "Exploring cliffside shops", "evening": "Seafood with a view"},
            {"day": 2, "title": "Island Escape", "morning": "Boat trip to Capri", "afternoon": "Blue Grotto visit", "evening": "Dinner in Anacapri"},
            {"day": 3, "title": "The Path of Gods", "morning": "Sentiero degli Dei hike", "afternoon": "Ravello gardens", "evening": "Limoncello tasting"}
        ]
    },
    {
        "city": "Singapore",
        "country": "Singapore",
        "vibes": ["Foodie", "Luxury", "Fashion"],
        "tagline": "A tropical city-state of the future and hawker feasts.",
        "estimated_cost": "$2,400",
        "itinerary": [
            {"day": 1, "title": "The Future", "morning": "Gardens by the Bay", "afternoon": "Cloud Forest & Flower Dome", "evening": "Marina Bay Sands light show"},
            {"day": 2, "title": "Hawker Culture", "morning": "Maxwell Food Centre", "afternoon": "Orchard Road shopping", "evening": "Clarke Quay nightlife"},
            {"day": 3, "title": "Island Fun", "morning": "Sentosa Island", "afternoon": "Universal Studios", "evening": "Night Safari at the Zoo"}
        ]
    },
    {
        "city": "Patagonia",
        "country": "Chile/Argentina",
        "vibes": ["Nature", "Aloof", "Offbeat"],
        "tagline": "End of the world glaciers and jagged peaks.",
        "estimated_cost": "$2,600",
        "itinerary": [
            {"day": 1, "title": "Glacier Majesty", "morning": "Perito Moreno boat tour", "afternoon": "Ice trekking", "evening": "Patagonian lamb roast"},
            {"day": 2, "title": "Towers of Granite", "morning": "Torres del Paine hike", "afternoon": "Wildlife spotting", "evening": "Cozy mountain lodge rest"},
            {"day": 3, "title": "Lakes & Forests", "morning": "Lake Pehoe sunrise", "afternoon": "Grey Glacier viewpoint", "evening": "Stargazing in the wild"}
        ]
    }
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    user_vibes = set(data.get("vibes", []))
    budget = int(data.get("budget", 10000))

    matches = []
    for dest in DESTINATIONS:
        dest_vibes = set(dest["vibes"])
        overlap = len(user_vibes.intersection(dest_vibes))
        cost = int(dest["estimated_cost"].replace("$", "").replace(",", ""))
        if cost <= budget:
            matches.append((overlap, dest))

    matches.sort(key=lambda x: x[0], reverse=True)
    top_destinations = [m[1] for m in matches[:3]]

    return jsonify({
        "destinations": top_destinations,
        "map_key": os.getenv("GOOGLE_MAPS_API_KEY", "")
    })


@app.route("/itinerary", methods=["POST"])
def itinerary():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    city      = data.get("city", "")
    country   = data.get("country", "")
    vibes     = data.get("vibes", [])
    travelers = data.get("travelers", 1)
    budget    = data.get("budget", 5000)

    prompt = (
        f"You are an expert travel planner. Generate a vivid, personalised 3-day itinerary "
        f"for {travelers} traveller(s) visiting {city}, {country}. "
        f"Their vibes: {', '.join(vibes)}. Total budget: ${budget} per person.\n\n"
        f"Respond ONLY with a valid JSON object, no markdown, no explanation.\n\n"
        f"Format:\n"
        f'{{"itinerary": ['
        f'{{"day": 1, "title": "...", "morning": "...", "afternoon": "...", "evening": "..."}}, '
        f'{{"day": 2, "title": "...", "morning": "...", "afternoon": "...", "evening": "..."}}, '
        f'{{"day": 3, "title": "...", "morning": "...", "afternoon": "...", "evening": "..."}}'
        f']}}'
    )

    gemini_key = os.getenv("GEMINI_API_KEY", "")
    if not gemini_key:
        return jsonify({"error": "Gemini API key not configured"}), 500

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={gemini_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 1024}
    }

    try:
        res = requests.post(url, json=payload, timeout=15)
        res.raise_for_status()
        raw = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        parsed = json.loads(clean)
        return jsonify(parsed)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
