import random
import string
import time
import requests
import allure

from requests.exceptions import RequestException

from urls import (
    CREATE_COURIER_URL,
    LOGIN_COURIER_URL,
    CREATE_ORDER_URL,
    ORDERS_LIST_URL,
    COURIER_BY_ID_URL
)

REQUEST_TIMEOUT = (5, 25)
RETRIES = 3
RETRY_DELAY = 1


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def request_with_retry(method, url, data=None, json=None):
    last_exception = None
    last_response = None

    for _ in range(RETRIES):
        try:
            response = requests.request(
                method=method,
                url=url,
                data=data,
                json=json,
                timeout=REQUEST_TIMEOUT
            )
            last_response = response

            if response.status_code < 500:
                return response

        except RequestException as exc:
            last_exception = exc

        time.sleep(RETRY_DELAY)

    if last_response is not None:
        return last_response

    raise last_exception


@allure.step("Сгенерировать данные нового курьера")
def generate_courier_payload():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }


@allure.step("Создать курьера")
def create_courier(payload):
    return request_with_retry("POST", CREATE_COURIER_URL, data=payload)


@allure.step("Авторизовать курьера")
def login_courier(payload):
    return request_with_retry("POST", LOGIN_COURIER_URL, json=payload)


@allure.step("Удалить курьера по id")
def delete_courier_by_id(courier_id):
    return requests.delete(
        COURIER_BY_ID_URL.format(courier_id=courier_id),
        timeout=REQUEST_TIMEOUT
    )


@allure.step("Создать заказ")
def create_order(payload):
    return request_with_retry("POST", CREATE_ORDER_URL, json=payload)


@allure.step("Получить список заказов")
def get_orders_list():
    return request_with_retry("GET", ORDERS_LIST_URL)