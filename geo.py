import pandas as pd
from geopy.geocoders import Nominatim
import time

def get_coordinates(commune, wilaya, country="Algeria"):
    geolocator = Nominatim(user_agent="geoapi_commune")
    location_name = f"{commune}, {wilaya}, {country}"
    try:
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Erreur pour {location_name} : {e}")
        return None, None

# Charger le CSV d'entrée
input_file = "no_coordinates.csv"
df = pd.read_csv(input_file)

# Créer deux nouvelles colonnes pour latitude et longitude
df["LATITUDE"] = None
df["LONGITUDE"] = None

# Obtenir les coordonnées pour chaque commune
for index, row in df.iterrows():
    lat, lon = get_coordinates(row["COMMUNE"], row["WILAYA"])
    df.at[index, "LATITUDE"] = lat
    df.at[index, "LONGITUDE"] = lon
    print(f"{row['COMMUNE']}, {row['WILAYA']} => {lat}, {lon}")
    time.sleep(1)  # Respecter les limites de l'API

# Sauvegarder le résultat dans un nouveau CSV
output_file = "communes_with_coordinates_added.csv"
df.to_csv(output_file, index=False)
print(f"Résultat sauvegardé dans : {output_file}")