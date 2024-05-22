# ライブラリをインポート
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf
from pandas_datareader import data as pdr
import datetime

# Yahoo!ファイナンスのデータをpandas-datareaderで扱う
yf.pdr_override()

# 銘柄のシンボル (米国株: META)
ticker_symbol = "META"

# 銘柄のシンボル (日本株の場合は「銘柄コード+.T」)
# ticker_symbol = "6526.T"

# 今日の日付を取得
today = datetime.date.today()

# 過去365日前の日付を取得
past_date = today - datetime.timedelta(days=365)

# 今日の日付を確認
print("Today:", today)

# 過去365日前の日付を確認
print("Past date:", past_date)

# データを取得 (日付、始値、高値、安値、終値、調整終値、出来高)
data = pdr.get_data_yahoo(ticker_symbol, start=str(past_date), end=str(today))

# データの型を確認
print(type(data))

# データの行数と列数を確認
print(data.shape)

# データを確認
print(data)

# データコピーして、データフレームに設定
df = data.copy()

# データの型を確認
print(type(df))

# データの行数と列数を確認
print(df.shape)

# データフレームにインデックス名を設定
df.index.name = "date"

# インデックスを日付に指定
date = df.index

# 日付を昇順に並び替える
df.sort_index(inplace=True)

# データを確認
print(df)

# 始値、高値、安値、終値の平均価格のカラム
df["Average_of_ohlc"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4

# 高値、安値、終値の平均価格のカラム
df["Average_of_hlc"] = (df["High"] + df["Low"] + df["Close"]) / 3

# 高値、安値の平均価格のカラム
df["Average_of_hl"] = (df["High"] + df["Low"]) / 2

# カラム(Average_of_ohlc、Average_of_hlc、Average_of_hl)が作成されているか確認
print(df.head())

# 平均価格を描画
plt.figure(figsize=(16,6))
plt.plot(df["Average_of_ohlc"], label="OHLC")
plt.plot(df["Average_of_hlc"], label="HLC")
plt.plot(df["Average_of_hl"], label="HL")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# HLバンド、中間線を作成
high = df["High"]
low = df["Low"]

# 20日のハイバンド
df["High_band"] = high.rolling(window=20).max()
# 20日のローバンド
df["Low_band"] = low.rolling(window=20).min()
# 中間線
df["Median_line"] = (df["High_band"] + df["Low_band"]) / 2

# カラム(High_band、Low_band、Median_line)が作成されているか確認
print(df.tail())

# ハイバンド、ローバンド、中間線を描画
plt.figure(figsize=(16,6))
plt.plot(df["High_band"], label="High")
plt.plot(df["Median_line"], label="Median")
plt.plot(df["Low_band"], label="Low")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# 20日移動平均線、200日移動平均線のカラムを作成
close = df["Close"]

# 20日移動平均線
df["Moving_average_of_20_days"] = close.rolling(window=20).mean()
# 200日移動平均線
df["Moving_average_of_200_days"] = close.rolling(window=200).mean()

# カラム(moving_average_of_20_days、moving_average_of_200_days)が作成されているか確認
print(df.tail())

# 20日移動平均線、200日移動平均線を描画
plt.figure(figsize=(16,6))
plt.plot(df["Moving_average_of_20_days"], label="20")
plt.plot(df["Moving_average_of_200_days"], label="200")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# ハイバンド、ローバンド、中間線、20日移動平均線、200日移動平均線、平均価格を描画
plt.figure(figsize=(16,6))
plt.plot(df["High_band"], label="High")
plt.plot(df["Low_band"], label="Low")
plt.plot(df["Median_line"], label="Median")
plt.fill_between(date, df["High_band"], df["Low_band"], facecolor="white", alpha=0.5, label="Span")
plt.plot(df["Moving_average_of_20_days"], label="20")
plt.plot(df["Moving_average_of_200_days"], label="200")
plt.plot(df["Average_of_ohlc"], label="OHLC")
plt.plot(df["Average_of_hlc"], label="HLC")
plt.plot(df["Average_of_hl"], label="HL")
plt.xlabel("Date")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# データフレームをExcelに出力
df.to_excel(ticker_symbol + "_hl_band_and_moving_average.xlsx")

# ローソク足を描画
mpf.plot(df, type="candle", figsize=(16,6), style="yahoo", xrotation=0)

# ローソク足、HLバンド、移動平均線、平均価格を描画する
lines = [
    mpf.make_addplot(df["High_band"], color="red", width=1.0),
    mpf.make_addplot(df["Median_line"], color="pink", width=0.5),
    mpf.make_addplot(df["Low_band"], color="blue", width=1.0),
    mpf.make_addplot(df["Moving_average_of_20_days"], color="green", width=1.0),
    mpf.make_addplot(df["Moving_average_of_200_days"], color="orange", width=1.0),
    mpf.make_addplot(df["Average_of_ohlc"], color="black", width=0.4)
]

labels = ["High", "Median", "Low", "200", "Ohlc"]
# labels = ["High", "Median", "Low", "20", "200", "Ohlc"]

fig, ax = mpf.plot(df, type="candle", figsize=(20,10), style="yahoo", xrotation=0, addplot=lines, returnfig=True)
# 描画せずグラフを保存する場合
# fig, ax = mpf.plot(df, type="candle", figsize=(20,10), style="yahoo", xrotation=0, addplot=lines, returnfig=True, savefig=ticker_symbol + ".png")

plt.show()

# ローソク足、HLバンド、移動平均線を描画する
lines = [
    mpf.make_addplot(df["High_band"], color="red", width=1.0),
    mpf.make_addplot(df["Median_line"], color="pink", width=0.5),
    mpf.make_addplot(df["Low_band"], color="blue", width=1.0),
    mpf.make_addplot(df["Moving_average_of_20_days"], color="green", width=1.0),
    mpf.make_addplot(df["Moving_average_of_200_days"], color="orange", width=1.0)
]

# labels = ["High", "Median", "Low", "200"]
labels = ["High", "Median", "Low", "20", "200"]

fig, ax = mpf.plot(df, type="candle", figsize=(20,10), style="yahoo", xrotation=0, addplot=lines, returnfig=True)
# 描画せずグラフを保存する場合
# fig, ax = mpf.plot(df, type="candle", figsize=(20,10), style="yahoo", xrotation=0, addplot=lines, returnfig=True, savefig=ticker_symbol + ".png")

plt.show()

# 銘柄のチャートを作成する関数
def create_chart(ticker_symbol, past_date, today):
    # データを取得 (日付、始値、高値、安値、終値、調整終値、出来高)
    data = pdr.get_data_yahoo(ticker_symbol, start=str(past_date), end=str(today))

    # データコピーして、データフレームに設定
    df = data.copy()

    # インデックスを日付に指定
    date = df.index

    # 日付を昇順に並び替える
    df.sort_index(inplace=True)

    # 始値、高値、安値、終値の平均価格のカラム
    df["Average_of_ohlc"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4

    # 高値、安値、終値の平均価格のカラム
    df["Average_of_hlc"] = (df["High"] + df["Low"] + df["Close"]) / 3

    # 高値、安値の平均価格のカラム
    df["Average_of_hl"] = (df["High"] + df["Low"]) / 2

    # HLバンド、中間線を作成
    high = df["High"]
    low = df["Low"]

    # 20日のハイバンド
    df["High_band"] = high.rolling(window=20).max()
    # 20日のローバンド
    df["Low_band"] = low.rolling(window=20).min()
    # 中間線
    df["Median_line"] = (df["High_band"] + df["Low_band"]) / 2

    # 20日移動平均線、200日移動平均線のカラムを作成
    close = df["Close"]

    # 20日移動平均線
    df["Moving_average_of_20_days"] = close.rolling(window=20).mean()
    # 200日移動平均線
    df["Moving_average_of_200_days"] = close.rolling(window=200).mean()

    # ローソク足、HLバンド、移動平均線、平均価格を描画する
    lines = [
        mpf.make_addplot(df["High_band"], color="red", width=1.0),
        mpf.make_addplot(df["Median_line"], color="pink", width=0.5),
        mpf.make_addplot(df["Low_band"], color="blue", width=1.0),
        mpf.make_addplot(df["Moving_average_of_20_days"], color="green", width=1.0),
        mpf.make_addplot(df["Moving_average_of_200_days"], color="orange", width=1.0),
        mpf.make_addplot(df["Average_of_ohlc"], color="black", width=0.4)
    ]

    labels = ["High", "Median", "Low", "20", "200", "Ohlc"]

    fig, ax = mpf.plot(df, type="candle", figsize=(20,10), style="yahoo", xrotation=0, addplot=lines, returnfig=True, savefig=ticker_symbol + "_chart.png")

# 銘柄のHLバンド、移動平均線のExcelを作成する関数
def create_hl_band_and_moving_average(ticker_symbol, past_date, today):
    # データを取得 (日付、始値、高値、安値、終値、調整終値、出来高)
    data = pdr.get_data_yahoo(ticker_symbol, start=str(past_date), end=str(today))

    # データコピーして、データフレームに設定
    df = data.copy()

    # インデックスを日付に指定
    date = df.index

    # 日付を昇順に並び替える
    df.sort_index(inplace=True)

    # 始値、高値、安値、終値の平均価格のカラム
    df["Average_of_ohlc"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4

    # 高値、安値、終値の平均価格のカラム
    df["Average_of_hlc"] = (df["High"] + df["Low"] + df["Close"]) / 3

    # 高値、安値の平均価格のカラム
    df["Average_of_hl"] = (df["High"] + df["Low"]) / 2

    # HLバンド、中間線を作成
    high = df["High"]
    low = df["Low"]

    # 20日のハイバンド
    df["High_band"] = high.rolling(window=20).max()
    # 20日のローバンド
    df["Low_band"] = low.rolling(window=20).min()
    # 中間線
    df["Median_line"] = (df["High_band"] + df["Low_band"]) / 2

    # 20日移動平均線、200日移動平均線のカラムを作成
    close = df["Close"]

    # 20日移動平均線
    df["Moving_average_of_20_days"] = close.rolling(window=20).mean()
    # 200日移動平均線
    df["Moving_average_of_200_days"] = close.rolling(window=200).mean()

    # データフレームをExcelに出力
    data_frame = df.to_excel(ticker_symbol + "_hl_band_and_moving_average_and_average_price.xlsx")

    return data_frame

# Yahoo!ファイナンスのデータをpandas-datareaderで扱う
yf.pdr_override()

# 米国株のシンボルのリスト (マグニフィセント・セブン)
symbols_list = [
    "AAPL",
    "AMZN",
    "GOOGL",
    "META",
    "MSFT",
    "NVDA",
    "TSLA"
]

# 今日の日付を取得
today = datetime.date.today()

# 過去365日前の日付を取得
past_date = today - datetime.timedelta(days=365)

# 今日の日付を確認
print("Today:", today)

# 過去365日前の日付を確認
print("Past date:", past_date)

# リストにあるシンボルのチャートを作成
for ticker_symbol in symbols_list:
    chart = create_chart(ticker_symbol, past_date, today)

# リストにあるシンボルのExcelを作成
for ticker_symbol in symbols_list:
    result = create_hl_band_and_moving_average(ticker_symbol, past_date, today)