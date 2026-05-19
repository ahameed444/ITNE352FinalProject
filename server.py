import socket
import threading
import json
from meal_api import MealAPI

class RecipeServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5555
        # Startup Behavior: Load reference cache once
        self.cache = self.startup_cache()

    def startup_cache(self):
        print("[SERVER] Initializing reference cache...")
        cats = MealAPI.get_categories()
        areas = MealAPI.get_areas()
        ingr = MealAPI.get_ingredients()
        
        cache_data = {
            "categories": cats,
            "areas": areas,
            "ingredients": {"meals": ingr.get("meals", [])[:50]} 
        }
        
        # FIXED: Named exactly 'reference.json'
        with open("reference.json", "w") as f:
            json.dump(cache_data, f, indent=4)
        print(f"[SERVER] Reference file created: reference.json")
        return {"categories": cats, "areas": areas, "ingredients": ingr}

    def handle_client(self, conn, addr):
        username = "Unknown"
        try:
            username = conn.recv(1024).decode()
            print(f"[NEW CONNECTION] {addr} connected. User: {username}")

            while True:
                data = conn.recv(4096).decode()
                if not data: break
                
                request = json.loads(data)
                option = request.get("option")

                if option == "QUIT":
                    break
                
                print(f"[REQUEST] {username} requested option: {option}")
                response = {}

                # Logic: Serve from Cache
                if option == "categories":
                    response = self.cache["categories"]
                elif option == "areas":
                    response = self.cache["areas"]
                elif option == "ingredients":
                    response = self.cache["ingredients"]
                
                # Fetch from API
                elif option == "1": # Search by name
                    response = MealAPI.search_by_name(request.get("parameter"))
                elif option == "2": # Filter by category
                    response = MealAPI.filter_by_category(request.get("parameter"))
                elif option == "5": # Random recipe
                    response = MealAPI.get_random()
                
                # FIXED: Named exactly '[username].json'
                if option in ["1", "2", "3", "4", "5"]:
                    filename = f"{username}.json"
                    with open(filename, "w") as f:
                        json.dump(response, f, indent=4)
                    print(f"[LOG] Data saved to {filename}")

                # Send data back to client
                conn.sendall(json.dumps(response).encode())

        except Exception as e:
            print(f"[ERROR] Handler failed for {username}: {e}")
        finally:
            print(f"[DISCONNECTED] {username} left the system.")
            conn.close()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[LISTENING] Server active on {self.host}:{self.port}...")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    RecipeServer().start()