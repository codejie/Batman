import pandas as pd
from app.calc import rsi

def test_rsi_calc_and_report():
    # Sample data that should produce some signals
    data = {
        '收盘': [
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, # Upward trend
            25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, # Strong upward trend (potential overbought)
            38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, # Downward trend
            23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9,  # Strong downward trend (potential oversold)
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 # Recovery
        ]
    }
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(pd.date_range(start='2023-01-01', periods=len(data['收盘'])))

    # Calculate RSI
    result_df = rsi.calc(df, options={'timeperiod': 14, 'column': '收盘'})

    # Assert columns exist
    assert 'RSI' in result_df.columns
    assert 'Signal' in result_df.columns

    # Check for NaN values at the beginning (due to timeperiod)
    assert result_df['RSI'].iloc[:13].isna().all()
    assert (result_df['Signal'].iloc[:13] == 0).all()

    # Check if signals are generated (at least some non-zero signals)
    assert any(result_df['Signal'] != 0)

    # Check signal values are -1, 0, or 1
    assert all(s in [-1, 0, 1] for s in result_df['Signal'].dropna())

    # Check report function
    report_data = rsi.report(df, result_df)
    assert isinstance(report_data, list)
    if report_data:
        assert 'index' in report_data[0]
        assert 'price' in report_data[0]
        assert 'trend' in report_data[0]
        assert all(item['trend'] in [-1, 1] for item in report_data) # Report only includes non-neutral signals

    print("RSI calculation and reporting test passed.")
