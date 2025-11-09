import pytest
import helpers.users as users


@pytest.fixture
def new_user_unregistered():
    new_user = users.new_user_data()
    email = new_user["email"]
    password = new_user["password"]
    yield new_user
    users.delete_user(email=email, password=password)


@pytest.fixture
def new_user_registered():
    new_user = users.register_new_user_and_return_email_password()
    token = new_user["accessToken"]
    yield new_user
    users.delete_user(token=token)


@pytest.fixture
def user_with_order():
    return users.user_with_orders()
