import requests
import allure
import pytest
from data.urls import BASE_URL, LOGIN
from data.users_test_data import USER_LOGIN_REQ_FIELDS


class TestUserLogin:
    URL = BASE_URL + LOGIN

    @allure.title("Проверка авторизации под существующим пользователем")
    def test_user_login_user_exists(self, new_user_registered):
        payload = {
            "email": new_user_registered["email"],
            "password": new_user_registered["password"]
        }
        response = requests.post(url=self.URL, data=payload)

        status_code_is_correct = response.status_code == 200
        response_body_is_correct = ((response.json()["success"] is True) and
                                    (response.json()["user"]["email"] == new_user_registered["email"]) and
                                    (response.json()["user"]["name"] == new_user_registered["name"]))

        assert status_code_is_correct and response_body_is_correct

    @allure.title("Проверка входа с неправильными данными. Некорректно передан: {param}")
    @pytest.mark.parametrize('param', USER_LOGIN_REQ_FIELDS)
    def test_user_login_incorrect_email_password(self, param, new_user_registered):
        url = BASE_URL + LOGIN
        payload = {
            "email": new_user_registered["email"],
            "password": new_user_registered["password"]
        }
        payload[param] += '_wrong!'

        response = requests.post(url=self.URL, data=payload)

        status_code_is_correct = response.status_code == 401
        response_body_is_correct = ((response.json()["success"] is False) and
                                    (response.json()["message"] == "email or password are incorrect"))

        assert status_code_is_correct and response_body_is_correct
