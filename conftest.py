import pytest
import allure

from helpers import (
    generate_courier_payload,
    create_courier,
    login_courier,
    delete_courier_by_id
)


@pytest.fixture
def courier_payload():
    return generate_courier_payload()


@pytest.fixture
def created_courier(courier_payload):
    response = create_courier(courier_payload)
    yield courier_payload, response


@pytest.fixture
def authorized_courier():
    courier = generate_courier_payload()
    create_response = create_courier(courier)

    courier_id = None
    login_response = login_courier({
        "login": courier["login"],
        "password": courier["password"]
    })

    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]

    yield {
        "courier": courier,
        "create_response": create_response,
        "login_response": login_response,
        "courier_id": courier_id
    }

    if courier_id is not None:
        with allure.step("Очистить тестовые данные: удалить курьера"):
            try:
                delete_courier_by_id(courier_id)
            except Exception:
                pass