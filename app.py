import csv
from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from spellchecker import SpellChecker

# Initialize the SpellChecker.
spell = SpellChecker()

# Load the custom dictionary from the CSV file "worldcities.csv".
# The CSV is assumed to have at least "city" and "country" columns.
custom_cities = []
with open("worldcities.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Filter only for Indian cities.
        if row.get("country") and row["country"].strip().lower() == "india":
            city = row.get("city")
            if city:
                custom_cities.append(city.strip())

# Load these custom city names into the SpellChecker's dictionary.
spell.word_frequency.load_words(custom_cities)

def correct_query(query):
    """
    Correct words in the input query using SpellChecker's correction.
    This will use our custom dictionary loaded from worldcities.csv.
    """
    corrected_words = []
    for word in query.split():
        corrected = spell.correction(word)
        corrected_words.append(corrected)
    return ' '.join(corrected_words)


app = Flask(__name__)

# Predefined list of properties with their latitudes and longitudes.
properties = [
    {"name": "Moustache Udaipur Luxuria", "latitude": 24.57799888, "longitude": 73.68263271},
    {"name": "Moustache Udaipur", "latitude": 24.58145726, "longitude": 73.68223671},
    {"name": "Moustache Udaipur Verandah", "latitude": 24.58350565, "longitude": 73.68120777},
    {"name": "Moustache Jaipur", "latitude": 27.29124839, "longitude": 75.89630143},
    {"name": "Moustache Jaisalmer", "latitude": 27.20578572, "longitude": 70.85906998},
    {"name": "Moustache Jodhpur", "latitude": 26.30365556, "longitude": 73.03570908},
    {"name": "Moustache Agra", "latitude": 27.26156953, "longitude": 78.07524716},
    {"name": "Moustache Delhi", "latitude": 28.61257139, "longitude": 77.28423582},
    {"name": "Moustache Rishikesh Luxuria", "latitude": 30.13769036, "longitude": 78.32465767},
    {"name": "Moustache Rishikesh Riverside Resort", "latitude": 30.10216117, "longitude": 78.38458848},
    {"name": "Moustache Hostel Varanasi", "latitude": 25.2992622, "longitude": 82.99691388},
    {"name": "Moustache Goa Luxuria", "latitude": 15.6135195, "longitude": 73.75705228},
    {"name": "Moustache Koksar Luxuria", "latitude": 32.4357785, "longitude": 77.18518717},
    {"name": "Moustache Daman", "latitude": 20.41486263, "longitude": 72.83282455},
    {"name": "Panarpani Retreat", "latitude": 22.52805539, "longitude": 78.43116291},
    {"name": "Moustache Pushkar", "latitude": 26.48080513, "longitude": 74.5613783},
    {"name": "Moustache Khajuraho", "latitude": 24.84602104, "longitude": 79.93139381},
    {"name": "Moustache Manali", "latitude": 32.28818695, "longitude": 77.17702523},
    {"name": "Moustache Bhimtal Luxuria", "latitude": 29.36552248, "longitude": 79.53481747},
    {"name": "Moustache Srinagar", "latitude": 34.11547314, "longitude": 74.88701741},
    {"name": "Moustache Ranthambore Luxuria", "latitude": 26.05471373, "longitude": 76.42953726},
    {"name": "Moustache Coimbatore", "latitude": 11.02064612, "longitude": 76.96293531},
    {"name": "Moustache Shoja", "latitude": 31.56341267, "longitude": 77.36733331}
]

# Initialize the geolocator (using a unique user_agent).
geolocator = Nominatim(user_agent="moustache_escapes")

@app.route("/api/properties", methods=["GET"])
def get_nearby_properties():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Correct minor spelling mistakes in the query.
    corrected_query = correct_query(query)
    
    try:
        location = geolocator.geocode(corrected_query, addressdetails=True, language='en')
        if not location:
            return jsonify({"message": "No properties available"}), 200
        query_location = (location.latitude, location.longitude)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    nearby_properties = []
    for prop in properties:
        prop_location = (prop["latitude"], prop["longitude"])
        distance = geodesic(query_location, prop_location).km
        if distance <= 50:
            nearby_properties.append({
                "property": prop["name"],
                "distance_km": round(distance, 2)
            })

    if not nearby_properties:
        return jsonify({"message": "No properties available"}), 200

    return jsonify({"properties": nearby_properties}), 200

if __name__ == "__main__":
    app.run(debug=True)