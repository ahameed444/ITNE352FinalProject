import requests

class MealAPI:
    BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

    @staticmethod
    def get_categories():
        return requests.get(f"{MealAPI.BASE_URL}list.php?c=list").json()

    @staticmethod
    def get_areas():
        return requests.get(f"{MealAPI.BASE_URL}list.php?a=list").json()

    @staticmethod
    def get_ingredients():
        return requests.get(f"{MealAPI.BASE_URL}list.php?i=list").json()

    @staticmethod
    def search_by_name(name):
        return requests.get(f"{MealAPI.BASE_URL}search.php?s={name}").json()

    @staticmethod
    def filter_by_category(category):
        return requests.get(f"{MealAPI.BASE_URL}filter.php?c={category}").json()

    @staticmethod
    def get_random():
        return requests.get(f"{MealAPI.BASE_URL}random.php").json()