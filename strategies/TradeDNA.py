# TradeDNA Strategy — Full Version

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
import talib.abstract as ta
import pandas as pd
import numpy as np

class TradeDNA(IStrategy):

    timeframe = "15m"

    minimal_roi = {
        "0": 0.03,
        "30": 0.02,
        "120": 0.01,
        "240": 0
    }

    stoploss = -0.10

    rsi_thresh = IntParameter(45, 55, default=50, space="buy")
    pullback_tolerance = DecimalParameter(0.001, 0.01, default=0.003, space="buy")
    elephant_factor = DecimalParameter(1.5, 3.0, default=2.0, space="buy")

    use_custom_stoploss = False

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:

        df["ema_high"] = ta.EMA(df["high"], timeperiod=20)
        df["ema_low"] = ta.EMA(df["low"], timeperiod=20)

        ha_close = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
        ha_open = ha_close.copy()
        ha_open.iloc[0] = (df["open"].iloc[0] + df["close"].iloc[0]) / 2
        for i in range(1, len(df)):
            ha_open.iloc[i] = (ha_open.iloc[i-1] + ha_close.iloc[i-1]) / 2

        df["ha_open"] = ha_open
        df["ha_close"] = ha_close
        df["ha_high"] = df[["high", "ha_open", "ha_close"]].max(axis=1)
        df["ha_low"] = df[["low", "ha_open", "ha_close"]].min(axis=1)

        df["ha_bull"] = df["ha_close"] > df["ha_open"]
        df["ha_bear"] = df["ha_close"] < df["ha_open"]

        df["rsi"] = ta.RSI(df, timeperiod=14)

        df["body"] = (df["close"] - df["open"]).abs()
        df["avg_body"] = df["body"].rolling(20).mean()
        df["elephant"] = df["body"] > (df["avg_body"] * float(self.elephant_factor.value))

        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:

        df.loc[
            (
                (df["ha_low"] > df["ema_high"]) &
                (df["ha_low"] > df["ema_low"]) &
                (df["ha_bull"]) &
                (df["rsi"] > int(self.rsi_thresh.value)) &
                (df["elephant"].rolling(5).max() == True) &
                ((df["close"] - df["ema_low"]).abs() / df["ema_low"] < float(self.pullback_tolerance.value))
            ),
            "buy"
        ] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:

        df.loc[
            (
                (df["ha_high"] < df["ema_high"]) &
                (df["ha_high"] < df["ema_low"]) &
                (df["ha_bear"]) &
                (df["rsi"] < int(self.rsi_thresh.value)) &
                (df["elephant"].rolling(5).max() == True) &
                ((df["close"] - df["ema_high"]).abs() / df["ema_high"] < float(self.pullback_tolerance.value))
            ),
            "sell"
        ] = 1

        return df
