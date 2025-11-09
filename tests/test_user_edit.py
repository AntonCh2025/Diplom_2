import requests
import allure
import pytest
from data.urls import BASE_URL, USER
from helpers.users import create_body_with_new_values_in_fields
from data.users_test_data import USER_EDIT_FIELDS


class TestUserEdit:
    URL = BASE_URL + USER

    @allure.title("Проверка изменения данных пользователя без авторизации. Редактируем: {fields}")
    @pytest.mark.parametrize('fields', USER_EDIT_FIELDS)
    def test_user_edit_unauthorised(self, fields, new_user_registered):
        payload = create_body_with_new_values_in_fields(fields, new_user_registered)

        response = requests.patch(url=self.URL, data=payload)
    
        status_code_is_correct = response.status_code == 401
        response_body_is_correct = ((response.json()["success"] is False) and
                                    (response.json()["message"] == "You should be authorised"))

        assert status_code_is_correct and response_body_is_correct

    @allure.title("Проверка изменения данных пользователя с авторизацией. Редактируем: {fields}")
    @pytest.mark.parametrize('fields', USER_EDIT_FIELDS)
    def test_user_edit_authorised(self, fields, new_user_registered):
        payload = create_body_with_new_values_in_fields(fields, new_user_registered)
        headers = {
            "authorization": new_user_registered["accessToken"]
        }

        response = requests.patch(url=self.URL, data=payload, headers=headers)

        status_code_is_correct = response.status_code == 200
        response_body_is_correct = (response.json()["success"] is True)
        
        assert status_code_is_correct and response_body_is_correct
