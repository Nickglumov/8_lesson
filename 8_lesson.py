import json
import requests
from geopy import distance
from pprint import pprint
import folium


APIKEY = "778295e1-90b2-41e5-bf3b-2f472d930a0c"


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lon, lat


def get_cafe_distance(cafe):
    return cafe["distance"]


def main():
    with open("coffee.json", "r") as my_file:
        file_contents = my_file.read()

    content = json.loads(file_contents)

    answer = input("Где вы находитесь? ")
    coords_str = fetch_coordinates(APIKEY, answer)

    coords = (float(coords_str[1]), float(coords_str[0]))

    cafes_with_distance = [
        {
            "title": cafe["Name"],
            "distance": distance.distance(coords, (cafe["Latitude_WGS84"], cafe["Longitude_WGS84"])).km,
            "latitude": cafe["Latitude_WGS84"],
            "longitude": cafe["Longitude_WGS84"],
        }
        for cafe in content
    ]

    sorted_cafe = sorted(cafes_with_distance, key=get_cafe_distance)

    m = folium.Map(location=[coords[0], coords[1]], zoom_start=14)

    for cafe in sorted_cafe[:5]:
        folium.Marker(
            location=[cafe["latitude"], cafe["longitude"]],
            tooltip="Click me!",
            popup=cafe["title"],
            icon=folium.Icon(color="green"),
        ).add_to(m)

    m.save("index.html")

    five_nearest = sorted_cafe[:5]
    pprint(five_nearest)


if __name__ == "__main__":
    main()