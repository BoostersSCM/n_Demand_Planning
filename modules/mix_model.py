import pandas as pd
import numpy as np

def compute_channel_item_mix(sales_hist: pd.DataFrame, channels: list[str]) -> pd.DataFrame:
    """채널별 품목 믹스 비율 계산"""
    df = sales_hist[sales_hist["channel"].isin(channels)].copy()
    if df.empty:
        return pd.DataFrame(columns=["channel", "product_code", "mix_ratio"])
    grp = df.groupby(["channel", "product_code"], as_index=False)["qty"].sum()
    grp["mix_ratio"] = grp.groupby("channel")["qty"].transform(lambda x: x / x.sum())
    return grp.fillna(0)
