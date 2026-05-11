import allure
import pytest

from helpers import create_order
from data import ORDER_BODY


class TestCreateOrder:

    @allure.title("Можно создать заказ с разными вариантами цвета")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors_returns_track(self, color):
        body = ORDER_BODY.copy()

        if color:
            body["color"] = color
        else:
            body.pop("color", None)

        response = create_order(body)

        assert response.status_code == 201
        assert "track" in response.json()