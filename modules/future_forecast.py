import pandas as pd
from .utils import get_relative_past_months

def predict_future_demand(kpi_df: pd.DataFrame, product_df: pd.DataFrame, sales_df: pd.DataFrame, target_month: str) -> pd.DataFrame:
    """
    KPI 목표 + 과거 판매비중 기반 미래 예측.
    - target_month: 'YYYY-MM'
    - sales_df가 비어있으면 경로 내 균등 분배로 대체
    """
    past_months = get_relative_past_months(target_month, 4)
    sales_recent = sales_df[sales_df['월'].isin(past_months)].copy()

    results = []

    # 경로 목록은 KPI에서 도출
    for _, kpi in kpi_df[kpi_df['월'] == target_month].iterrows():
        route = kpi['경로']
        kpi_sales = float(kpi['KPI매출'])

        route_products = product_df.copy()
        if '경로' in product_df.columns and product_df['경로'].notna().any():
            # 경로가 지정된 제품만 선택 (없으면 전체)
            route_products = product_df[(product_df['경로'] == route) | (product_df['경로'] == '')]

        # 판매비중 계산 (제품코드 우선)
        route_sales = sales_recent[sales_recent['경로'] == route]
        use_code = '제품코드' in route_sales.columns and route_sales['제품코드'].notna().any()

        if len(route_sales) > 0 and use_code:
            totals = route_sales.groupby('제품코드')['판매수량'].sum()
            denom = totals.sum()
        elif len(route_sales) > 0:
            totals = route_sales.groupby('제품명')['판매수량'].sum()
            denom = totals.sum()
        else:
            totals = None
            denom = 0

        n_products = max(1, len(route_products))
        for _, p in route_products.iterrows():
            price = float(p.get('판매가', 0) or 0)
            if price <= 0:
                # 가격 정보가 없으면 1로 가정하여 수량 배분
                price = 1.0

            ratio = 0.0
            if totals is not None and denom > 0:
                key = p['제품코드'] if use_code else p['제품명']
                ratio = float(totals.get(key, 0)) / float(denom)
            else:
                ratio = 1.0 / n_products

            predicted_qty = (kpi_sales * ratio) / price
            results.append({
                '월': target_month,
                '경로': route,
                '제품코드': p['제품코드'],
                '제품명': p['제품명'],
                '예측수량': round(predicted_qty, 0)
            })

    return pd.DataFrame(results)
