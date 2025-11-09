import requests
import allure
import pytest
from data.urls import BASE_URL, REGISTER
from data.users_test_data import USER_CREATE_REQ_FIELDS


class TestUserCreate:

    URL = BASE_URL + REGISTER

    @allure.title('Проверка создания уникального пользователя')
    def test_register_unique_user(self, new_user_unregistered):
        response = requests.post(url=self.URL, data=new_user_unregistered)

        status_code_is_correct = response.status_code == 200
        response_body_is_correct = ((response.json()["success"] is True) and
                                    (response.json()["user"]["email"] == new_user_unregistered["email"]) and
                                    (response.json()["user"]["name"] == new_user_unregistered["name"]))

        assert status_code_is_correct and response_body_is_correct

    @allure.title('Проверка создания пользователя с уже существующими данными')
    def test_register_user_registered_user_already_exists(self, new_user_registered):
        response = requests.post(url=self.URL, data=new_user_registered)

        status_code_is_correct = response.status_code == 403
        response_body_is_correct = ((response.json()["success"] is False) and
                                    (response.json()["message"] == "User already exists"))

        assert status_code_is_correct and response_body_is_correct

    @allure.title("Проверка создания пользователя с отсутствующими обязательными полями. Отсутствует: {param}")
    @pytest.mark.parametrize('param', USER_CREATE_REQ_FIELDS)
    def test_register_user_required_fields_missing(self, param, new_user_unregistered):
        payload = new_user_unregistered
        del payload[param]

        response = requests.post(url=self.URL, data=payload)

        status_code_is_correct = response.status_code == 403
        response_body_is_correct = ((response.json()["success"] is False) and
                                    (response.json()["message"] == "Email, password and name are required fields"))

        assert status_code_is_correct and response_body_is_correct
