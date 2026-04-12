import requests

# Base URL for the JSONPlaceholder API
BASE_URL = "https://jsonplaceholder.typicode.com"

def run_api_drill():
    # --- PART 1: POSTS ---
    print("--- PART 1: POSTS ---")
    
    # 1. Get All Posts (GET)
    response = requests.get(f"{BASE_URL}/posts")
    print(f"1. Status: {response.status_code}, Count: {len(response.json())}")

    # 2. Get Post by ID (Path Param)
    response = requests.get(f"{BASE_URL}/posts/1")
    print(f"2. JSON Body: {response.json()}")

    # 3. Get Posts by User (Query Param)
    # Using params={} as required (no hardcoded strings in URL)
    response = requests.get(f"{BASE_URL}/posts", params={"userId": 1})
    titles = [post['title'] for post in response.json()]
    print(f"3. User 1 Titles: {titles}")

    # 4. Create Post (POST + JSON Body)
    payload = {"title": "New Post", "body": "Content", "userId": 1}
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    print(f"4. Status: {response.status_code}, Response: {response.json()}")

    # 5. Update Post (PUT - Full replacement)
    update_payload = {"id": 1, "title": "Updated", "body": "Updated Body", "userId": 1}
    response = requests.put(f"{BASE_URL}/posts/1", json=update_payload)
    print(f"5. Full Response: {response.json()}")

    # 6. Patch Post (PATCH - Partial update)
    response = requests.patch(f"{BASE_URL}/posts/1", json={"title": "Patched Title"})
    print(f"6. Only Title: {response.json().get('title')}")

    # 7. Delete Post (DELETE)
    response = requests.delete(f"{BASE_URL}/posts/1")
    print(f"7. Status Only: {response.status_code}")

    # 8. Get Comments for Post (Nested URL)
    response = requests.get(f"{BASE_URL}/posts/1/comments")
    emails = [comment['email'] for comment in response.json()]
    print(f"8. Emails: {emails}")

    # --- PART 2: COMMENTS ---
    print("\n--- PART 2: COMMENTS ---")
    
    # 1. Get All
    response = requests.get(f"{BASE_URL}/comments")
    print(f"1. Count: {len(response.json())}")

    # 3. Filter by Post (Query Param)
    response = requests.get(f"{BASE_URL}/comments", params={"postId": 1})
    print(f"3. Emails: {[c['email'] for c in response.json()]}")

    # --- PART 4: PHOTOS ---
    print("\n--- PART 4: PHOTOS ---")
    
    # 1. Get All (Print first 5)
    response = requests.get(f"{BASE_URL}/photos")
    print(f"1. First 5: {response.json()[:5]}")

    # 3. Filter by Album (Query Param)
    response = requests.get(f"{BASE_URL}/photos", params={"albumId": 1})
    urls = [photo['url'] for photo in response.json()]
    print(f"3. URLs: {urls[:3]}...")

    # --- PART 5: TODOS ---
    print("\n--- PART 5: TODOS ---")
    
    # 4. Filter by Completed (Boolean Param)
    response = requests.get(f"{BASE_URL}/todos", params={"completed": True})
    print(f"4. Completed Titles: {[t['title'] for t in response.json()][:3]}...")

    # 6. Patch Todo
    response = requests.patch(f"{BASE_URL}/todos/1", json={"completed": False})
    print(f"6. JSON: {response.json()}")

    # --- PART 6: USERS ---
    print("\n--- PART 6: USERS ---")
    
    # 1. Get All (Nested data extraction)
    response = requests.get(f"{BASE_URL}/users")
    for user in response.json()[:2]:
        print(f"Name: {user['name']}, Email: {user['email']}")

    # 2. Get by ID (Deep JSON extraction)
    response = requests.get(f"{BASE_URL}/users/1")
    print(f"2. City: {response.json()['address']['city']}")

    # 3. Posts by User (Nested URL)
    response = requests.get(f"{BASE_URL}/users/1/posts")
    print(f"3. Titles: {[p['title'] for p in response.json()][:2]}...")

if __name__ == "__main__":
    run_api_drill()