import requests
import random
import string
import data.urls as urls


# метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def random_domain():
    domains = ['@mail.ru', '@yandex.ru', '@gmail.com', '@git.hub']
    return random.choice(domains)


def generate_random_email():
    return f'{generate_random_string(10)}{random_domain()}'


def new_user_data():
    user_data = {
        "email": generate_random_email(),
        "name": generate_random_string(15),
        "password": generate_random_string(20)
    }
    return user_data


def register_new_user_and_return_email_password():
    # гененрируем емейл, имя и пароль для регистрации нового пользователя
    user_data = new_user_data()
    # отправляем запрос на регистрацию
    url = urls.BASE_URL + urls.REGISTER
    response = requests.post(url=url, data=user_data)
    if response.status_code == 200:
        user_data["accessToken"] = response.json()["accessToken"]
        return user_data
    else:
        return {
            "code": response.status_code
        }


def delete_user(email=None, password=None, token=None):
           
    if (email is not None) and (password is not None):
        url = urls.BASE_URL + urls.LOGIN    
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(url=url, data=payload)
        if response.status_code == 200:
            token = response.json()["accessToken"]
    
    if token is not None:
        url = urls.BASE_URL + urls.USER
        headers = {
            "Authorization": token
        }
        response = requests.delete(url=url, headers=headers)


def create_body_with_new_values_in_fields(fields, body):
    new_body = {}
    for field in fields:
        if field == 'email':
            new_value = 'new_email@yahoo.by'
        else:
            new_value = f'field_edited_{generate_random_string(5)}'

        new_body[field] = new_value
    return new_body

def user_with_orders():
    payload = {
        "password": "Anton2025",
        "email": "anton2025@ya.ru"
    }
    url = urls.BASE_URL + urls.LOGIN
    response = requests.post(url=url, data=payload)
    if response.status_code == 200:
        user_token = response.json()["accessToken"]
        return user_token
    