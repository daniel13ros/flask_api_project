import requests

# Base URL for the PokeAPI
BASE_URL = "https://pokeapi.co/api/v2"

def run_pokeapi_lab():
    print("--- PHASE 5: BASIC REQUESTS ---")
    
    # 1. Get a list of Pokemon (Default pagination)
    # This identifies the resource structure
    response = requests.get(f"{BASE_URL}/pokemon")
    data = response.json()
    print(f"1. Total Pokemon count in API: {data['count']}")
    print(f"   First Pokemon in list: {data['results'][0]['name']}")

    # 2. Get a specific Pokemon (Path Param)
    # Deep JSON exploration
    pokemon_name = "pikachu"
    response = requests.get(f"{BASE_URL}/pokemon/{pokemon_name}")
    pokemon_data = response.json()
    print(f"2. {pokemon_name.capitalize()} weight: {pokemon_data['weight']}")
    
    # --- PHASE 6: RESOURCE RELATIONSHIPS ---
    print("\n--- PHASE 6: RELATIONSHIPS & LINKS ---")
    
    # Extracting a link to another resource from the response
    # Follow the 'species' link
    species_url = pokemon_data['species']['url']
    print(f"Linking to species resource: {species_url}")
    
    species_res = requests.get(species_url)
    print(f"Species Generation: {species_res.json()['generation']['name']}")

    # --- PHASE 7: PAGINATION & QUERY PARAMS ---
    print("\n--- PHASE 7: PAGINATION ---")
    
    # Using 'limit' and 'offset' as identified in the documentation
    params = {
        "limit": 5,
        "offset": 10
    }
    response = requests.get(f"{BASE_URL}/pokemon", params=params)
    paged_data = response.json()
    
    print(f"Next page URL provided by API: {paged_data['next']}")
    print(f"Current page items: {[p['name'] for p in paged_data['results']]}")

    # --- ADVANCED CHALLENGE: THE CHAIN FLOW ---
    print("\n--- ADVANCED CHALLENGE: CHAINED REQUESTS ---")
    
    # 1. Get Pokemon basic info
    char_res = requests.get(f"{BASE_URL}/pokemon/charizard")
    char_data = char_res.json()
    
    # 2. Extract the first ability and its URL
    ability_name = char_data['abilities'][0]['ability']['name']
    ability_url = char_data['abilities'][0]['ability']['url']
    print(f"Charizard Ability: {ability_name}")
    
    # 3. Request the ability resource to see which other Pokemon share it
    ability_res = requests.get(ability_url)
    others = [p['pokemon']['name'] for p in ability_res.json()['pokemon'][:5]]
    print(f"Other Pokemon with {ability_name}: {others}")

    # --- PHASE 10: PATTERN RECOGNITION ---
    print("\n--- PHASE 10: PATTERNS ---")
    # Patterns show that many resources use the same /resource/id structure
    resources = ["type/1", "ability/4", "berry/1"]
    for r in resources:
        res = requests.get(f"{BASE_URL}/{r}")
        if res.status_code == 200:
            print(f"Endpoint confirmed: {BASE_URL}/{r} -> {res.json().get('name')}")

if __name__ == "__main__":
    run_pokeapi_lab()