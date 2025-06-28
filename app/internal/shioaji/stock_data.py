"""
Shioaji data retrieval service for stock scanners and snapshots.
All functions are pure and use dependency injection for API and constants.
Do NOT initialize or login Shioaji API in this module; inject api/sj from outside.
"""

import pandas as pd

from app.configs.config import get_config
from app.utils.logger import log

config = get_config()


def get_shioaji_scanners(api, sj, count: int = 200) -> pd.DataFrame:
    """
    Retrieve scanner data from Shioaji API.
    Args:
        api: Shioaji API instance (injected).
        sj: Shioaji module/constant (injected).
        count (int): Number of stocks to scan.
    Returns:
        pd.DataFrame: Scanner data.
    """
    scanners = api.scanners(
        scanner_type=sj.constant.ScannerType.AmountRank, count=count
    )
    if not scanners:
        log.warning("[Shioaji] scanners is empty.")
        return pd.DataFrame()
    df_scanners = pd.DataFrame(s.__dict__ for s in scanners)
    if df_scanners.empty:
        log.warning("[Shioaji] df_scanners is empty.")
        return pd.DataFrame()
    df_scanners["ts"] = pd.to_datetime(df_scanners["ts"])
    return df_scanners


def get_shioaji_snapshots(api, contracts) -> pd.DataFrame:
    """
    Retrieve snapshot data from Shioaji API.
    Args:
        api: Shioaji API instance (injected).
        contracts: List of Shioaji contracts.
    Returns:
        pd.DataFrame: Snapshot data.
    """
    if not contracts:
        log.warning("[Shioaji] contracts is empty.")
        return pd.DataFrame()
    snapshots = api.snapshots(contracts)
    if not snapshots:
        log.warning("[Shioaji] snapshots is empty.")
        return pd.DataFrame()
    df_snapshots = pd.DataFrame(s.__dict__ for s in snapshots)
    if df_snapshots.empty:
        log.warning("[Shioaji] df_snapshots is empty.")
        return pd.DataFrame()
    df_snapshots["ts"] = pd.to_datetime(df_snapshots["ts"])
    return df_snapshots


def get_filtered_stocks(api, sj) -> pd.DataFrame:
    """
    Filter stocks using Shioaji API and return a DataFrame of filtered stock info.
    Args:
        api: Shioaji API instance (injected).
        sj: Shioaji module/constant (injected).
    Returns:
        pd.DataFrame: Filtered stock info.
    """
    try:
        df_scanners = get_shioaji_scanners(api, sj)
        if df_scanners.empty:
            log.warning("[Shioaji] No scanner data available.")
            return pd.DataFrame()
        contracts = [api.Contracts.Stocks[code] for code in df_scanners["code"]]
        if not contracts:
            log.warning("[Shioaji] No contracts available.")
            return pd.DataFrame()
        df_snapshots = get_shioaji_snapshots(api, contracts)
        if df_snapshots.empty:
            log.warning("[Shioaji] No snapshot data available.")
            return pd.DataFrame()
        filtered_df = df_snapshots[
            (df_snapshots["total_volume"] >= 1.1 * df_snapshots["yesterday_volume"])
        ].copy()
        if filtered_df.empty:
            log.warning("[Shioaji] No stocks matched filter condition.")
            return pd.DataFrame()

        def determine_yf_code(row):
            if row["exchange"] == "TSE":
                return f"{row['code']}.TW"
            elif row["exchange"] == "OTC":
                return f"{row['code']}.TWO"
            else:
                return None

        filtered_df["yf_code"] = filtered_df.apply(determine_yf_code, axis=1)
        result_df = pd.merge(
            filtered_df, df_scanners[["code", "name"]], on="code", how="left"
        )
        if result_df.empty:
            log.warning("[Shioaji] No merged result data.")
            return pd.DataFrame()
        result_df = result_df[["yf_code", "name", "change_rate"]].copy()
        return result_df
    except Exception as e:
        log.error(f"Error in get_filtered_stocks: {e}")
        return pd.DataFrame()
