import pytest
from datetime import datetime, timedelta
from assessment_app.utils.utils import compute_cagr, datetime_to_str, str_to_datetime
from assessment_app.models.constants import DAYS_IN_YEAR


def test_compute_cagr_valid():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 1, 1)
    beginning_value = 1000
    ending_value = 1331

    expected_years = (end_date - start_date).days / DAYS_IN_YEAR
    expected_cagr = ((ending_value / beginning_value) ** (1 / expected_years) - 1) * 100

    result = compute_cagr(beginning_value, ending_value, start_date, end_date)
    assert round(result, 2) == round(expected_cagr, 2)


def test_compute_cagr_invalid_beginning_value():
    with pytest.raises(ValueError, match="Beginning value must be greater than zero."):
        compute_cagr(0, 1000, datetime(2020, 1, 1), datetime(2021, 1, 1))


def test_compute_cagr_invalid_ending_value():
    with pytest.raises(ValueError, match="Ending value must be greater than zero."):
        compute_cagr(1000, 0, datetime(2020, 1, 1), datetime(2021, 1, 1))


def test_compute_cagr_invalid_dates():
    with pytest.raises(ValueError, match="Start date must be before end date."):
        compute_cagr(1000, 1200, datetime(2021, 1, 1), datetime(2020, 1, 1))


def test_datetime_to_str():
    dt = datetime(2024, 5, 17)
    assert datetime_to_str(dt) == "2024-05-17"


def test_str_to_datetime():
    date_str = "2024-05-17"
    dt = str_to_datetime(date_str)
    assert dt == datetime(2024, 5, 17)


def test_str_to_datetime_and_back():
    date_str = "2023-12-25"
    dt = str_to_datetime(date_str)
    assert datetime_to_str(dt) == date_str
