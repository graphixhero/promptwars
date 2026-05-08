import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Mock Data for Tokyo
MOCK_FLIGHTS = [
    {
        "airline": "Japan Airlines",
        "departure": "10:00 AM",
        "arrival": "2:00 PM",
        "duration": "14h 0m",
        "price": "$1,200",
        "stops": "Non-stop"
    },
    {
        "airline": "All Nippon Airways",
        "departure": "12:30 PM",
        "arrival": "4:45 PM",
        "duration": "14h 15m",
        "price": "$1,350",
        "stops": "Non-stop"
    },
    {
        "airline": "United Airlines",
        "departure": "8:15 AM",
        "arrival": "3:20 PM",
        "duration": "17h 5m",
        "price": "$950",
        "stops": "1 stop (SFO)"
    }
]

MOCK_ITINERARY = [
    {
        "day": 1,
        "title": "Modern Tokyo & Neon Lights",
        "morning": "Explore Shibuya Crossing and Hachiko Statue.",
        "afternoon": "Visit Harajuku's Takeshita Street and Meiji Jingu Shrine.",
        "evening": "Dinner in Shinjuku and city views from the Metropolitan Government Building."
    },
    {
        "day": 2,
        "title": "Tradition & Culture",
        "morning": "Asakusa Senso-ji Temple and Nakamise Shopping Street.",
        "afternoon": "Boat cruise on Sumida River to Odaiba.",
        "evening": "Sushi dinner at Tsukiji Outer Market area."
    },
    {
        "day": 3,
        "title": "Hidden Gems & Art",
        "morning": "Ghibli Museum (requires booking) or Inokashira Park.",
        "afternoon": "Art galleries in Roppongi Hills or Mori Art Museum.",
        "evening": "Izakaya hopping in Golden Gai."
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    return jsonify({
        "flights": MOCK_FLIGHTS,
        "itinerary": MOCK_ITINERARY,
        "map_key": os.getenv("GOOGLE_MAPS_API_KEY", "")
    })

if __name__ == "__main__":
    app.run(debug=True)
