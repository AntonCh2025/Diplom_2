import requests
import allure

from data.urls import BASE_URL, ORDERS


class TestGetUserOrders:
    URL = BASE_URL + ORDERS

    @allure.title("Проверка получения заказов пользователя. Пользователь не авторизован")
    def test_get_user_orders_unauthorised(self):
 
        response = requests.get(url=self.URL)

        status_code_is_correct = response.status_code == 401
        response_body_is_correct = ((response.json()["success"] is False) and
                                    (response.json()["message"] == "You should be authorised"))

        assert status_code_is_correct and response_body_is_correct

    @allure.title("Проверка получения заказов пользователя. Пользователь авторизован, заказов нет.")
    def test_get_user_orders_authorised_orders_empty(self, new_user_registered):
        headers = {
            "authorization": new_user_registered["accessToken"]
        }

        response = requests.get(url=self.URL, headers=headers)

        status_code_is_correct = response.status_code == 200
        response_body_is_correct = ((response.json()["success"] is True) and
                                    (response.json()["orders"] == []))
        
        assert status_code_is_correct and response_body_is_correct

    
    @allure.title("Проверка получения заказов пользователя. Пользователь авторизован, заказы есть.")
    def test_get_user_orders_orders_not_empty(self, user_with_order):

        headers = {
            "authorization": user_with_order
        }

        response = requests.get(url=self.URL, headers=headers)

        status_code_is_correct = response.status_code == 200
        response_body_is_correct = ((response.json()["success"] is True) and
                                    (len(response.json()["orders"]) >0))
        
        assert status_code_is_correct and response_body_is_correct
