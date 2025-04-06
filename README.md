# 🏙️ City-Based Property Search API

This Flask API allows users to search for properties near a misspelled city name using spell correction and geolocation. It supports fuzzy matching of Indian city names and returns a list of nearby properties within a 50km radius.

---

## 🚀 Features

- ✅ Corrects misspelled Indian city names using `pyspellchecker`
- ✅ Uses the `IndiaCities.csv` as the city database
- ✅ Geocodes corrected city names using the `geopy` Nominatim API
- ✅ Filters nearby properties within a 50 km radius
- ✅ Returns property names with distance in kilometers

---

## 📦 Dependencies

Install all dependencies using pip:

```bash
pip install flask geopy pyspellchecker
```

---

## 📁 File Structure

```plaintext
project/
│
├── app.py               # Main Flask application
├── IndiaCities.csv      # Database of Indian city names
└── README.md            # This file
```

---

## 🔧 How to Run

1. Ensure Python is installed.
2. Clone/download this project.
3. Run the Flask server:

```bash
python app.py
```

The API will be available at:  
```
http://127.0.0.1:5000/api/properties
```

---

## 🔍 API Usage

### Endpoint

```
GET /api/properties?query=<city_name>
```

### Query Parameters

| Parameter | Type   | Description                     |
|-----------|--------|---------------------------------|
| `query`   | string | Misspelled or correct city name |

### Example

```bash
curl "http://127.0.0.1:5000/api/properties?query=delih"
```

### Response

```json
{
  "properties": [
    {
      "property": "Moustache Delhi",
      "distance_km": 3.75
    }
  ]
}
```

If no properties are found:

```json
{
  "message": "No properties available"
}
```

---

## 🧠 How It Works

- The city name is spell-checked using the [`pyspellchecker`](https://github.com/barrust/pyspellchecker) library.
- It uses city names from `IndiaCities.csv` to correct possible errors.
- Once corrected, it is geocoded using the Nominatim API.
- Then we calculate the distance of this location from a list of predefined properties.
- Properties within 50 km are returned.

---

## ✨ Example City Corrections

| Input     | Corrected |
|-----------|-----------|
| `delih`   | `delhi`   |
| `bangalre`| `bangalore` |
| `mumbay`  | `mumbai`  |

---

## 🛠️ Todo / Improvements

- Add support for multiple countries or global city lists.
- Use caching for repeated geocode queries.
- Add confidence level for spelling corrections.

---

## 📬 Contact

For questions or support, feel free to reach out to [Swagat Nayak](mailto:swagat.nayak.cd.che21@itbhu.ac.in)

