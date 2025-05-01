import math
import numpy as np
from typing import List, Dict, Any
from enum import Enum
from statistics import mean, median, mode, variance


class StatisticalOperation(str, Enum):
    MEAN = "mean"
    MEDIAN = "median"
    MODE = "mode"
    VARIANCE = "variance"
    IS_NORMAL = "is_normally_distributed"
    LINEAR_REGRESSION = "linear_regression"


class StatsService:
    SUPPORTED_OPERATIONS = {op.value for op in StatisticalOperation}

    @staticmethod
    def calculate(
        data: List[Dict[str, Any]],
        column: str,
        operation: StatisticalOperation,
        target_column: str = None,
    ) -> Dict[str, Any]:
        if operation not in StatisticalOperation:
            raise ValueError(f"Unsupported operation: '{operation}'")

        match operation:
            case StatisticalOperation.MEAN:
                return StatsService.calculate_mean(data, column)
            case StatisticalOperation.MEDIAN:
                return StatsService.calculate_median(data, column)
            case StatisticalOperation.MODE:
                return StatsService.calculate_mode(data, column)
            case StatisticalOperation.VARIANCE:
                return StatsService.calculate_variance(data, column)
            case StatisticalOperation.IS_NORMAL:
                return StatsService.is_normally_distributed(data, column)
            case StatisticalOperation.LINEAR_REGRESSION:
                if not target_column:
                    raise ValueError("Linear regression requires a 'target_column'")
                return StatsService.linear_regression(data, column, target_column)

    @staticmethod
    def calculate_mean(data: List[Dict[str, Any]], column: str) -> Dict[str, float]:
        values = StatsService.extract_numeric_values(data, column)
        return {"mean": mean(values)}

    @staticmethod
    def calculate_median(data: List[Dict[str, Any]], column: str) -> Dict[str, float]:
        values = StatsService.extract_numeric_values(data, column)
        return {"median": median(values)}

    @staticmethod
    def calculate_mode(data: List[Dict[str, Any]], column: str) -> Dict[str, float]:
        values = StatsService.extract_numeric_values(data, column)
        return {"mode": mode(values)}

    @staticmethod
    def calculate_variance(data: List[Dict[str, Any]], column: str) -> Dict[str, float]:
        values = StatsService.extract_numeric_values(data, column)
        return {"variance": variance(values)}

    @staticmethod()
    def is_normally_distributed(
        data: List[Dict[str, Any]], column: str
    ) -> Dict[str, Any]:
        values = StatsService.extract_numeric_values(data, column)
        mean_value = mean(values)
        standard_deviation = math.sqrt(variance(values))
        count = len(values)
        within_one_standard_deviations = (
            sum(
                mean_value - standard_deviation <= x <= mean_value + standard_deviation
                for x in values
            )
            / count
        )
        within_two_standard_deviations = (
            sum(
                mean_value - 2 * standard_deviation
                <= x
                <= mean_value + 2 * standard_deviation
                for x in values
            )
            / count
        )

        return {
            "approximated_normal": within_one_standard_deviations > 0.68
            and within_two_standard_deviations > 0.95,
            "within_1sd": within_one_standard_deviations,
            "within_2sd": within_two_standard_deviations,
        }

    @staticmethod
    def extract_numeric_values(data: List[Dict[str, Any]], column: str) -> List[float]:
        values = [
            row[column] for row in data if isinstance(row.get(column), (int, float))
        ]

        if not values:
            raise ValueError(f"No valid numeric values found in column '{column}'")

        return values

    @staticmethod
    def linear_regression(
        data: List[Dict[str, Any]], feature_column: str, target_column: str
    ) -> Dict[str, float]:
        x_values = [
            row[feature_column]
            for row in data
            if isinstance(row.get(feature_column), (int, float))
            and isinstance(row.get(target_column), (int, float))
        ]
        y_values = [
            row[target_column]
            for row in data
            if isinstance(row.get(feature_column), (int, float))
            and isinstance(row.get(target_column), (int, float))
        ]

        if len(x_values) < 2:
            raise ValueError("Insufficient data points for linear regression")

        x = np.array(x_values)
        y = np.array(y_values)

        x_mean = np.mean(x)
        y_mean = np.mean(y)

        slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
        intercept = y_mean - slope * x_mean

        y_pred = slope * x + intercept
        ss_total = np.sum((y - y_mean) ** 2)
        ss_res = np.sum((y - y_pred) ** 2)
        r_squared = 1 - (ss_res / ss_total)

        return {"slope": slope, "intercept": intercept, "r_squared": r_squared}
