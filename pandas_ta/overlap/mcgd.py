# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, verify_series
from pandas import Series


def mcgd(close: Series, length: int = None, offset: int = None, c: float = None, **kwargs) -> Series:
    """McGinley Dynamic Indicator

    The McGinley Dynamic looks like a moving average line, yet it is actually a
    smoothing mechanism for prices that minimizes price separation, price whipsaws,
    and hugs prices much more closely. Because of the calculation, the Dynamic Line
    speeds up in down markets as it follows prices yet moves more slowly in up
    markets. The indicator was designed by John R. McGinley, a Certified Market
    Technician and former editor of the Market Technicians Association's Journal
    of Technical Analysis.

    Sources:
        https://www.investopedia.com/articles/forex/09/mcginley-dynamic-indicator.asp

    Args:
        close (pd.Series): Series of 'close's
        length (int): Indicator's period. Default: 10
        c (float): Multiplier for the denominator, sometimes set to 0.6. Default: 1
        offset (int): Number of periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate arguments
    length = int(length) if length and length > 0 else 10
    c = float(c) if c and 0 < c <= 1 else 1
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None: return

    # Calculate Result
    close = close.copy()

    def mcg_(series):
        denom = (c * length * (series[1] / series[0]) ** 4)
        series[1] = (series[0] + ((series[1] - series[0]) / denom))
        return series[1]

    mcg_cell = close[0:].rolling(2, min_periods=2).apply(mcg_, raw=True)
    mcg_ds = close[:1].append(mcg_cell[1:])

    # Offset
    if offset != 0:
        mcg_ds = mcg_ds.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        mcg_ds.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        mcg_ds.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    mcg_ds.name = f"MCGD_{length}"
    mcg_ds.category = "overlap"

    return mcg_ds
