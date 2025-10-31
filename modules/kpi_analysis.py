import pandas as pd
from .future_forecast import predict_future_demand

def evaluate_past_accuracy(kpi_df: pd.DataFrame, product_df: pd.DataFrame, sales_df: pd.DataFrame, month: str) -> pd.DataFrame:
    """KPI 기반 예측 vs 실제 비교 (month: 'YYYY-MM')."""
    forecast = predict_future_demand(kpi_df, product_df, sales_df, month)
    actual = sales_df[sales_df['월'] == month][['경로','제품코드','제품명','판매수량']].copy()

    # 병합 우선순위: 제품코드, 없으면 제품명
    if '제품코드' in forecast.columns and forecast['제품코드'].notna().any():
        merged = pd.merge(forecast, actual, on=['경로','제품코드'], how='left')
    else:
        merged = pd.merge(forecast, actual, on=['경로','제품명'], how='left')

    merged['판매수량'] = merged['판매수량'].fillna(0).astype(float)
    merged['오차(수량)'] = (merged['예측수량'] - merged['판매수량']).abs()
    merged['정확도(%)'] = merged.apply(
        lambda r: 100.0 if r['판매수량'] == 0 and r['예측수량'] == 0
        else max(0.0, 100.0 - (abs(r['예측수량'] - r['판매수량']) / max(1.0, r['판매수량'])) * 100.0),
        axis=1
    )
    return merged[['월','경로','제품코드','제품명','예측수량','판매수량','정확도(%)']]
