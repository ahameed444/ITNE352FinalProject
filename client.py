import socket
import json

class RecipeClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.valid_categories = ["Beef", "Chicken", "Seafood", "Vegetarian", "Dessert", "Pasta", "Breakfast"]
        self.valid_areas = ["Italian", "Indian", "Mexican", "Japanese", "Moroccan", "British", "American", "Thai"]

    def recv_all(self):
        """Helper to safely receive complete, un-truncated JSON data streams from the server."""
        BUFF_SIZE = 4096
        data = b""
        while True:
            part = self.socket.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.decode()

    def start(self):
        try:
            self.socket.connect((self.host, self.port))
            username = input("Enter your username: ")
            self.socket.send(username.encode())
            
            while True:
                print("\n--- Main Menu ---")
                print("1. Browse Recipes")
                print("2. Reference Lists")
                print("3. Quit")
                choice = input("Select an option: ")
                
                if choice == "1": 
                    self.recipe_menu()
                elif choice == "2": 
                    self.reference_menu()
                elif choice == "3":
                    self.socket.send(json.dumps({"option": "QUIT"}).encode())
                    break
                else:
                    print("Invalid choice.")
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            self.socket.close()

    def recipe_menu(self):
        while True:
            print("\n--- Recipes Menu ---")
            print("1. Search by name")
            print("2. Filter by category")
            print("3. Filter by area")
            print("4. Filter by ingredient")
            print("5. Random recipe")
            print("6. Back to main menu")
            choice = input("Select an option: ")
            
            if choice == "6": 
                break
                
            request = {"option": choice}
            
            if choice == "2":
                print(f"Permitted: {', '.join(self.valid_categories)}")
                val = input("Enter category: ")
                if val not in self.valid_categories: 
                    print("Invalid category!")
                    continue
                request["parameter"] = val
            elif choice == "3":
                print(f"Permitted: {', '.join(self.valid_areas)}")
                val = input("Enter area: ")
                if val not in self.valid_areas: 
                    print("Invalid area!")
                    continue
                request["parameter"] = val
            elif choice == "1": 
                request["parameter"] = input("Enter keyword: ")
            elif choice == "4": 
                request["parameter"] = input("Enter ingredient: ").strip().replace(" ", "_")
            elif choice == "5": 
                request["parameter"] = ""

            # Transmit structured request
            self.socket.send(json.dumps(request).encode())
            
            # Safely parse full response stream
            try:
                response_json = self.recv_all()
                response = json.loads(response_json)
                self.display_results(response)
            except Exception as e:
                print(f"Error handling recipe data: {e}")

    def reference_menu(self):
        while True:
            print("\n--- Reference Menu ---")
            print("1. List all categories")
            print("2. List all areas")
            print("3. List all ingredients")
            print("4. Back to main menu")
            choice = input("Select an option: ")
            
            if choice == "4": 
                break
                
            options = {"1": "categories", "2": "areas", "3": "ingredients"}
            if choice in options:
                self.socket.send(json.dumps({"option": options[choice]}).encode())
                try:
                    response_json = self.recv_all()
                    response = json.loads(response_json)
                    print(json.dumps(response, indent=2))
                except Exception as e:
                    print(f"Error handling reference data: {e}")

    def display_results(self, data):
        """Displays cleanly formatted results instead of a raw text dump."""
        if "meals" in data and data["meals"]:
            meals_list = data["meals"]
            print(f"\n=================== FOUND {len(meals_list)} RESULTS (Showing Max 15) ===================")
            for meal in meals_list[:15]:
                meal_id = meal.get('idMeal')
                name = meal.get('strMeal')
                print(f" -> ID: {meal_id:<6} | Name: {name}")
            print("==========================================================================")
        else:
            print("\n[INFO] No results found matching your query.")

if __name__ == "__main__":
    RecipeClient().start()