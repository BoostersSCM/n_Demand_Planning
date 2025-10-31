import pandas as pd
import numpy as np

def analyze_trend(sales_df: pd.DataFrame, months_back: int = 6) -> pd.DataFrame:
    """제품별 최근 판매 추세 분석 (경로 무시하고 제품 단위로 통합)."""
    # 최신 N개월만 사용
    unique_months = sorted(sales_df['월'].dropna().unique())
    if not unique_months:
        return pd.DataFrame(columns=['제품명','변화율(%)','추세'])
    months = unique_months[-months_back:]

    df = sales_df[sales_df['월'].isin(months)].copy()
    # 제품별 월별 합계
    pivot = df.pivot_table(index='제품명', columns='월', values='판매수량', aggfunc='sum', fill_value=0)

    rows = []
    for prod in pivot.index:
        series = pivot.loc[prod]
        if len(series) < 3:
            recent_avg = series.mean()
            past_avg = series.mean()
        else:
            k = len(series)
            recent = series.iloc[-2:] if k >= 2 else series
            past = series.iloc[:-2] if k >= 3 else series
            recent_avg = recent.mean()
            past_avg = past.mean()

        change = 0.0 if past_avg == 0 else ((recent_avg - past_avg) / past_avg) * 100.0
        status = '상승' if change > 5 else ('하락' if change < -5 else '안정')
        rows.append({'제품명': prod, '변화율(%)': round(change,1), '추세': status})

    return pd.DataFrame(rows).sort_values(by=['추세','변화율(%)'], ascending=[True, False])
