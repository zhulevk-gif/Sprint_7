import allure

from helpers import create_courier
from data import (
    COURIER_CREATED_RESPONSE,
    CREATE_COURIER_NOT_ENOUGH_DATA_MESSAGE,
    CREATE_COURIER_DUPLICATE_MESSAGE
)


class TestCreateCourier:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, courier_payload):
        response = create_courier(courier_payload)

        assert response.status_code == 201
        assert response.json() == COURIER_CREATED_RESPONSE

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_returns_error(self, courier_payload):
        first_response = create_courier(courier_payload)
        second_response = create_courier(courier_payload)

        assert first_response.status_code == 201
        assert second_response.status_code == 409
        assert second_response.json()["message"] == CREATE_COURIER_DUPLICATE_MESSAGE

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login_returns_error(self, courier_payload):
        courier_payload.pop("login")

        response = create_courier(courier_payload)

        assert response.status_code == 400
        assert response.json()["message"] == CREATE_COURIER_NOT_ENOUGH_DATA_MESSAGE

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password_returns_error(self, courier_payload):
        courier_payload.pop("password")

        response = create_courier(courier_payload)

        assert response.status_code == 400
        assert response.json()["message"] == CREATE_COURIER_NOT_ENOUGH_DATA_MESSAGE