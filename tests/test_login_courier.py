import allure

from helpers import login_courier
from data import LOGIN_NOT_ENOUGH_DATA_MESSAGE, LOGIN_WRONG_DATA_MESSAGE


class TestLoginCourier:

    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login(self, authorized_courier):
        response = authorized_courier["login_response"]

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Нельзя авторизоваться без логина")
    def test_login_without_login_returns_error(self):
        response = login_courier({
            "password": "testpassword"
        })

        assert response.status_code == 400
        assert response.json()["message"] == LOGIN_NOT_ENOUGH_DATA_MESSAGE

    @allure.title("Система вернет ошибку при неверном логине")
    def test_login_with_wrong_login_returns_error(self, authorized_courier):
        courier = authorized_courier["courier"]

        response = login_courier({
            "login": "wronglogin",
            "password": courier["password"]
        })

        assert response.status_code == 404
        assert response.json()["message"] == LOGIN_WRONG_DATA_MESSAGE

    @allure.title("Система вернет ошибку при неверном пароле")
    def test_login_with_wrong_password_returns_error(self, authorized_courier):
        courier = authorized_courier["courier"]

        response = login_courier({
            "login": courier["login"],
            "password": "wrongpassword"
        })

        assert response.status_code == 404
        assert response.json()["message"] == LOGIN_WRONG_DATA_MESSAGE

    @allure.title("Нельзя авторизоваться под несуществующим пользователем")
    def test_login_nonexistent_courier_returns_error(self):
        response = login_courier({
            "login": "notexistlogin",
            "password": "notexistpassword"
        })

        assert response.status_code == 404
        assert response.json()["message"] == LOGIN_WRONG_DATA_MESSAGE