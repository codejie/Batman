import pandas as pd
import talib
from typing import List, Dict, Any

def get_ma_trend(historical_data: pd.DataFrame, ma_periods: List[int]) -> Dict[str, Any]:
    """
    根据提供的历史数据和移动平均线(MA)周期，计算MA值并判断当前趋势。

    Args:
        historical_data (pd.DataFrame): 包含历史价格数据的数据集。
                                         必须包含一个名为 'close' 的列。
        ma_periods (List[int]): 一个包含两个或多个整数的列表，代表要计算的MA周期。
                                通常第一个是短期，第二个是长期。

    Returns:
        Dict[str, Any]: 一个包含以下信息的字典:
                        - 'ma_values': 一个包含每个周期最新MA值的字典。
                        - 'trend': 一个表示当前趋势的字符串 ("Uptrend", "Downtrend", "Sideways")。
                        - 'analysis': 对趋势的简要文字描述。
    """
    if not isinstance(historical_data, pd.DataFrame) or 'close' not in historical_data.columns:
        raise ValueError("historical_data 必须是一个包含 'close' 列的 pandas DataFrame")

    if not isinstance(ma_periods, list) or len(ma_periods) < 2:
        raise ValueError("ma_periods 必须是一个至少包含两个周期的列表")

    # 确保周期是整数并排序
    ma_periods = sorted([int(p) for p in ma_periods])
    short_period = ma_periods[0]
    long_period = ma_periods[-1]

    # 检查是否有足够的数据来计算最长的MA
    if len(historical_data) < long_period:
        return {
            "ma_values": {},
            "trend": "Not Enough Data",
            "analysis": f"需要至少 {long_period} 条数据来计算MA({long_period})，但只有 {len(historical_data)} 条。"
        }

    df = historical_data.copy()

    # 使用 talib 计算所有指定的MA
    for period in ma_periods:
        df[f'MA_{period}'] = talib.MA(df['close'].values, timeperiod=period)

    # 获取最新的数据行
    latest_data = df.iloc[-1]

    # 提取最新的MA值
    ma_values = {f'MA_{p}': round(latest_data[f'MA_{p}'], 2) for p in ma_periods if pd.notna(latest_data[f'MA_{p}'])}

    # 判断趋势
    latest_short_ma = ma_values.get(f'MA_{short_period}')
    latest_long_ma = ma_values.get(f'MA_{long_period}')
    
    trend = "Sideways"
    analysis = f"短期MA({short_period})与长期MA({long_period})非常接近。"

    if latest_short_ma and latest_long_ma:
        if latest_short_ma > latest_long_ma:
            trend = "Uptrend"
            analysis = f"短期MA({short_period})在长期MA({long_period})之上，表明市场处于上升趋势。"
        elif latest_short_ma < latest_long_ma:
            trend = "Downtrend"
            analysis = f"短期MA({short_period})在长期MA({long_period})之下，表明市场处于下降趋势。"

    return {
        "ma_values": ma_values,
        "trend": trend,
        "analysis": analysis
    }

def ma_diff_rank(data: pd.Series, periods: list[int], ma_type: int = talib.MA_Type.SMA) -> int:
	periods = sorted(periods)
	if len(periods) < 2:
		raise ValueError("必须提供至少两个MA周期")
	if periods[-1] > len(data):
		raise ValueError(f"数据长度不足以计算最长MA周期: {periods[-1]}")
	# ma_data: Dict[int, float] = {}
	ma_data: list[float] = [data.iloc[-1]]
	for period in periods:
		ma_data.append(talib.MA(data.values, timeperiod=period, matype=ma_type)[-1])
	
	rank = 0
	for i in range(0, len(ma_data) - 1):
		if ma_data[i] > ma_data[i+1]:
			rank += 1
		elif ma_data[i] < ma_data[i+1]:
			rank -= 1

	return rank

def ma_diff_rank_rate(periods: list[int], rank: int) -> float:
	range = len(periods)
	return (rank + range) / (2 * range) * 9
		
#####################
def ma_trend_rank(data: pd.Series, periods: list[int], ma_type: int = talib.MA_Type.SMA) -> int:
	"""
	计算MA趋势排名
	:param data: 数据序列
	:param periods: MA周期列表
	:param ma_type: MA类型
	:return: MA趋势排名
	"""
	return ma_diff_rank(data, periods, ma_type)

