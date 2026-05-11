import allure

from helpers import get_orders_list


class TestOrdersList:

    @allure.title("В тело ответа возвращается список заказов")
    def test_get_orders_list_returns_orders_list(self):
        response = get_orders_list()

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)