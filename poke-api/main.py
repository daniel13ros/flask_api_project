import requests

DATA_URL = "https://pokeapi.co/api/v2/berry/1"

data = requests.get(DATA_URL).json()
print(data)
print(data["id"])
print(data["name"])
print(data["growth_time"])
print(data["max_harvest"])
print(data["natural_gift_power"])