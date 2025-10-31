import streamlit as st
import pandas as pd
from modules.data_manager import load_products, load_kpi, load_sales_history
from modules.future_forecast import predict_future_demand
from modules.kpi_analysis import evaluate_past_accuracy
from modules.trend_analysis import analyze_trend

st.set_page_config(page_title="이퀄베리 예측 대시보드 (DB)", page_icon="📊", layout="wide")
st.title("📊 이퀄베리 수요 예측 대시보드 — DB Rebuild")

with st.sidebar:
    st.header("⚙️ 설정")

# Load data
with st.spinner("DB에서 데이터 로딩 중..."):
    products = load_products()
    kpi = load_kpi()
    sales = load_sales_history(months_back=6)

st.success("데이터 로딩 완료")

# Month options (YYYY-MM)
month_options = sorted(kpi['월'].dropna().unique())
default_month = month_options[-1] if month_options else None

tab1, tab2, tab3 = st.tabs(["🔮 미래 예측", "📏 KPI 정확도", "📉 판매 추세"])

with tab1:
    st.subheader("🔮 KPI 기반 미래 예측")
    target_month = st.selectbox("예측 대상 월 (YYYY-MM)", month_options, index=len(month_options)-1 if month_options else 0)
    if target_month:
        forecast_df = predict_future_demand(kpi, products, sales, target_month)
        st.dataframe(forecast_df, use_container_width=True)
    else:
        st.info("KPI 데이터가 없습니다. monthly_kpi 테이블을 확인해주세요.")

with tab2:
    st.subheader("📏 과거 KPI 예측 vs 실제")
    compare_month = st.selectbox("비교 월 (YYYY-MM)", month_options, index=max(0, len(month_options)-2))
    if compare_month:
        compare_df = evaluate_past_accuracy(kpi, products, sales, compare_month)
        st.dataframe(compare_df, use_container_width=True)
        st.caption("※ 판매수량이 비어있거나 0인 경우 정확도 계산이 안전하게 처리되도록 되어 있습니다.")
    else:
        st.info("KPI 데이터가 없습니다. monthly_kpi 테이블을 확인해주세요.")

with tab3:
    st.subheader("📉 최근 판매 추세")
    trend_df = analyze_trend(sales, months_back=6)
    st.dataframe(trend_df, use_container_width=True)
    st.caption("최근 2개월 vs 그 이전 평균을 비교하여 상승/안정/하락을 분류합니다.")
