from __future__ import annotations
from loguru import logger

from typing import TYPE_CHECKING, Literal, Callable
# if TYPE_CHECKING:


class DistanceFunctionFactory:
    @staticmethod
    def create_distance_function_via_name(
        distance_function_name: Literal[
            'MAE', 'MSE', 'RMSE',
        ],
    ) -> Callable[..., float]:
        if distance_function_name == 'MAE':
            return DistanceFunctionFactory.create_mas_function()
        elif distance_function_name == 'MSE':
            return DistanceFunctionFactory.create_mse_function()
        elif distance_function_name == 'RMSE':
            return DistanceFunctionFactory.create_rmse_function()
        else:
            raise ValueError(f"Unsupported Distance Function: {distance_function_name}")

    @staticmethod
    def create_mas_function() -> Callable[..., float]:
        def calculate_mean_absolute_error(
            y_true: list[float],
            y_pred: list[float],
            distance_func_kwargs: dict | None = None,
        ) -> float:
            assert len(y_true) == len(y_pred)
            error = 0
            for i in range(len(y_true)):
                error += abs(y_true[i] - y_pred[i])
            return error / len(y_true)
        logger.debug(f"Create mean absolute error function.")
        return calculate_mean_absolute_error

    @staticmethod
    def create_mse_function() -> Callable[..., float]:
        def calculate_mean_squared_error(
            y_true: list[float],
            y_pred: list[float],
            distance_func_kwargs: dict | None = None,
        ) -> float:
            assert len(y_true) == len(y_pred)
            error = 0
            for i in range(len(y_true)):
                error += (y_true[i] - y_pred[i])**2
            return error / len(y_true)
        logger.debug(f"Create mean squared error function.")
        return calculate_mean_squared_error

    @staticmethod
    def create_rmse_function() -> Callable[..., float]:
        def calculate_root_mean_squared_error(
            y_true: list[float],
            y_pred: list[float],
            distance_func_kwargs: dict | None = None,
        ) -> float:
            raise NotImplementedError
        raise NotImplementedError

