from data.urls import BASE_URL, INGREDIENTS
import requests
import random


def get_ingredients():
    url = BASE_URL + INGREDIENTS
    response = requests.get(url=url)
    buns = sauces = fillings = []
    ingredients = {}

    if response.status_code == 200:
        for id in response.json()["data"]:
            if id["type"] == "bun":
                buns.append(id["_id"])
            elif id["type"] == "sauce":
                sauces.append(id["_id"])
            elif id["type"] == "main":
                fillings.append(id["_id"])

    ingredients["buns"] = buns
    ingredients["sauces"] = sauces
    ingredients["fillings"] = fillings

    return ingredients

def prepare_burger_receipt():
    receipt = []
    ingredients = get_ingredients()
    receipt.append(random.choice(ingredients["buns"]))
    receipt.append(random.choice(ingredients["fillings"]))
    receipt.append(random.choice(ingredients["sauces"]))

    return receipt
