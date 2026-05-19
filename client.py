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
                print("\n--- Main Menu ---\n1. Browse Recipes\n2. Reference Lists\n3. Quit")
                choice = input("Select an option: ")
                if choice == "1": self.recipe_menu()
                elif choice == "2": self.reference_menu()
                elif choice == "3":
                    self.socket.send(json.dumps({"option": "QUIT"}).encode())
                    break
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            self.socket.close()

    def recipe_menu(self):
        while True:
            print("\n--- Recipes Menu ---\n1. Search by name\n2. Filter by category\n3. Filter by area\n4. Filter by ingredient\n5. Random recipe\n6. Back")
            choice = input("Select an option: ")
            if choice == "6": break
            request = {"option": choice}
            if choice == "2":
                val = input("Enter category: ")
                if val not in self.valid_categories: continue
                request["parameter"] = val
            elif choice == "1": request["parameter"] = input("Enter keyword: ")
            elif choice == "5": request["parameter"] = ""
            
            self.socket.send(json.dumps(request).encode())
            print(json.loads(self.recv_all()))

    def reference_menu(self):
        while True:
            print("\n--- Reference Menu ---\n1. Categories\n2. Areas\n3. Ingredients\n4. Back")
            choice = input("Select an option: ")
            if choice == "4": break
            options = {"1": "categories", "2": "areas", "3": "ingredients"}
            if choice in options:
                self.socket.send(json.dumps({"option": options[choice]}).encode())
                print(json.loads(self.recv_all()))

if __name__ == "__main__":
    RecipeClient().start()