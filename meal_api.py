import requests

class MealAPI:
    """
    This class handles all communication with TheMealDB API.
    It isolates the 'On-demand API fetching' pattern required by the project.
    """
    
    BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

    @staticmethod
    def get_categories():
        """Fetches the list of all meal categories[cite: 32]."""
        response = requests.get(f"{MealAPI.BASE_URL}list.php?c=list")
        return response.json()

    @staticmethod
    def get_areas():
        """Fetches the list of all cuisines/areas[cite: 33]."""
        response = requests.get(f"{MealAPI.BASE_URL}list.php?a=list")
        return response.json()

    @staticmethod
    def get_ingredients():
        """Fetches the list of all ingredients[cite: 34]."""
        response = requests.get(f"{MealAPI.BASE_URL}list.php?i=list")
        return response.json()

    @staticmethod
    def search_by_name(name):
        """Searches for recipes by name keyword[cite: 78]."""
        response = requests.get(f"{MealAPI.BASE_URL}search.php?s={name}")
        return response.json()

    @staticmethod
    def filter_by_category(category):
        """Filters recipes by a specific category[cite: 78]."""
        response = requests.get(f"{MealAPI.BASE_URL}filter.php?c={category}")
        return response.json()

    @staticmethod
    def get_random():
        """Fetches a single random recipe with full details[cite: 78, 86]."""
        response = requests.get(f"{MealAPI.BASE_URL}random.php")
        return response.json()

    @staticmethod
    def get_details(meal_id):
        """Fetches full details for a specific meal ID[cite: 96]."""
        response = requests.get(f"{MealAPI.BASE_URL}lookup.php?i={meal_id}")
        return response.json()