import requests
import allure

from data.urls import BASE_URL, ORDERS
from helpers.orders import prepare_burger_receipt


class TestOrderCreate:
    url = BASE_URL + ORDERS

    @allure.title("Проверка создания заказа с ингредиентами, пользователь неавторизован")
    def test_order_create_unauthorised_user_with_ingredients(self):
        payload = {"ingredients": prepare_burger_receipt()}
        response = requests.post(url=self.url, json=payload)

        status_code_is_correct = response.status_code == 200
        response_body_is_correct = ((response.json()["success"] is True) and
                                    ("owner" not in response.json()["order"].keys()))
        
        assert status_code_is_correct and response_body_is_correct
        
    @allure.title("Проверка создания заказа без ингредиентов, пользователь неавторизован")
    def test_order_create_unauthorised_user_withouth_ingredients(self):
        payload = {"ingredients": []}

        response = requests.post(url=self.url, data=payload)

        status_code_is_correct = response.status_code == 400
        response_body_is_correct = ((response.json()["success"] is False) and
                                    (response.json()["message"] == 'Ingredient ids must be provided'))
        
        assert status_code_is_correct and response_body_is_correct
  
    @allure.title("Проверка создания заказа с неправильным хэшем ингредиентов, пользователь неавторизован")
    def test_order_create_unauthorised_user_wrong_ingredients(self):
        payload = {"ingredients": ["qwe123", "123qwe", "some_hash"]}

        response = requests.post(url=self.url, data=payload)

        status_code_is_correct = response.status_code == 500
        
        assert status_code_is_correct

    @allure.title("Проверка создания заказа с ингредиентами, пользователь авторизован")
    def test_order_create_authorised_user_with_ingredients(self, new_user_registered):
        payload = {"ingredients": prepare_burger_receipt()}

        headers = {"authorization": new_user_registered["accessToken"]}

        response = requests.post(url=self.url, json=payload, headers=headers)

        status_code_is_correct = response.status_code == 200
        response_body_is_correct = ((response.json()["success"] is True) and
                                    ("owner" in response.json()["order"].keys()))
        
        assert status_code_is_correct and response_body_is_correct

    @allure.title("Проверка создания заказа без ингредиентов, пользователь авторизован")
    def test_order_create_authorised_user_withouth_ingredients(self, new_user_registered):
        payload = {"ingredients": []}
        headers = {"authorization": new_user_registered["accessToken"]}

        response = requests.post(url=self.url, data=payload, headers=headers)

        status_code_is_correct = response.status_code == 400
        response_body_is_correct = ((response.json()["success"] is False) and
                                    (response.json()["message"] == 'Ingredient ids must be provided'))
        
        assert status_code_is_correct and response_body_is_correct

    @allure.title("Проверка создания заказа с неправильным хэшем ингредиентов, пользователь авторизован")
    def test_order_create_authorised_user_wrong_ingredients(self, new_user_registered):
        payload = {"ingredients": ["qwe123", "123qwe", "some_hash"]}
        headers = {"authorization": new_user_registered["accessToken"]}

        response = requests.post(url=self.url, data=payload, headers=headers)

        status_code_is_correct = response.status_code == 500
        
        assert status_code_is_correct
