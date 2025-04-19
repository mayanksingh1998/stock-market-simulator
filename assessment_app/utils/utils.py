from datetime import datetime
from assessment_app.models.constants import DAYS_IN_YEAR


def compute_cagr(beginning_value: float, ending_value: float, start_date: datetime, end_date: datetime) -> float:
    """
    Compute the Compound Annual Growth Rate (CAGR).

    Returns:
        float: The CAGR in percentage. (e.g., 12.0 for 12%)
    """
    if beginning_value <= 0:
        raise ValueError("Beginning value must be greater than zero.")
    if ending_value <= 0:
        raise ValueError("Ending value must be greater than zero.")
    if start_date >= end_date:
        raise ValueError("Start date must be before end date.")

    duration_days = (end_date - start_date).days
    years = duration_days / DAYS_IN_YEAR
    cagr = ((ending_value / beginning_value) ** (1 / years) - 1) * 100
    return round(cagr, 2)


def datetime_to_str(dt: datetime) -> str:
    """
    Convert a datetime object to a string in the format 'YYYY-MM-DD'.
    """
    return dt.strftime('%Y-%m-%d')


def str_to_datetime(date_str: str) -> datetime:
    """
    Convert a string in the format 'YYYY-MM-DD' to a datetime object.
    """
    return datetime.strptime(date_str, '%Y-%m-%d')
