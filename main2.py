import requests
import yfinance as yf
import pandas as pd
import datetime
from bs4 import BeautifulSoup
DISCLAIMER_TEXT = """
---------------------------------------------------------------
DISCLAIMER   (Please Scroll Down and Read it Completely)
---------------------------------------------------------------
The information, data, charts, indicators, and analytics provided by this stock monitoring system are strictly for educational, informational, and research purposes only. They do not constitute investment advice, trading advice, or recommendations to buy, sell, or hold any securities.

This system only displays publicly available market data and calculated indicators derived from such data sources. The analysis, indicators, and signals generated are automated outputs and should not be considered as financial or investment advice.

The developer/owner of this system is not registered with the Securities and Exchange Board of India (SEBI) as an Investment Adviser or Research Analyst. Therefore, users should not rely solely on the information provided here for making investment or trading decisions.

Investments in the stock market are subject to market risks, including the possible loss of principal. Users are strongly advised to conduct their own research (DYOR) and consult a SEBI-registered investment adviser or financial professional before making any investment decisions.

This application is created for learning and fun purposes only.

By accessing or using this system, you acknowledge that all investment and trading decisions are taken at your own risk.
"""
SIGNATURE_TEXT = "Welcome to 🐝BuzyBeeStocks By Aryan\nTwitter @BuzyStocks75531 @MasterTrader49X"
class BuzyBee:
    def fetch_nse(self, symbol):
        try:
            session = requests.Session()
            headers = {"User-Agent": "Mozilla/5.0"}
            session.get("https://www.nseindia.com", headers=headers)
            url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
            r = session.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                return r.json()
        except:
            return None
    def fetch_yahoo(self, symbol):
        try:
            ticker = yf.Ticker(symbol + ".NS")
            info = ticker.info
            hist = ticker.history(period="1y")
            return info, hist
        except:
            return None, None
    def fetch_screener(self, symbol):
        try:
            url = f"https://www.screener.in/company/{symbol}/"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            return soup.text
        except:
            return None
    def SMA(self, df, n):
        return df["Close"].rolling(n).mean().iloc[-1]
    def RSI(self, df, n=14):
        delta = df["Close"].diff()
        gain = (delta.where(delta>0,0)).rolling(n).mean()
        loss = (-delta.where(delta<0,0)).rolling(n).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    def Bollinger(self, df, n=20):
        sma = df["Close"].rolling(n).mean()
        std = df["Close"].rolling(n).std()
        upper = sma + (2*std)
        lower = sma - (2*std)
        return upper.iloc[-1], lower.iloc[-1]
    def VWAP(self, df):
        vwap = (df["Close"] * df["Volume"]).cumsum() / df["Volume"].cumsum()
        return vwap.iloc[-1]
    def ATR(self, df, n=14):
        df["H-L"] = df["High"] - df["Low"]
        df["H-PC"] = abs(df["High"] - df["Close"].shift())
        df["L-PC"] = abs(df["Low"] - df["Close"].shift())
        tr = df[["H-L","H-PC","L-PC"]].max(axis=1)
        atr = tr.rolling(n).mean()
        return atr.iloc[-1]
    def Volatility(self, df):
        returns = df["Close"].pct_change()
        vol = returns.std() * 252 ** 0.5
        return vol
    def get_stock_info(self, symbol):
        symbol = symbol.strip().upper()
        if not symbol:
            return "Enter Stock Symbol"
        nse = self.fetch_nse(symbol)
        info, hist = self.fetch_yahoo(symbol)
        screener = self.fetch_screener(symbol)
        if hist is None or hist.empty:
            return "Unable to fetch stock data"
        last = hist.iloc[-1]
        ltp = last["Close"]
        prev_close = hist["Close"].iloc[-2]
        openp = last["Open"]
        high = last["High"]
        low = last["Low"]
        volume = last["Volume"]
        sma20 = self.SMA(hist, 20)
        sma50 = self.SMA(hist, 50)
        sma100 = self.SMA(hist, 100)
        sma200 = self.SMA(hist, 200)
        rsi = self.RSI(hist)
        bb_upper, bb_lower = self.Bollinger(hist)
        vwap = self.VWAP(hist)
        atr = self.ATR(hist)
        volatility = self.Volatility(hist)
        wk_high = hist["High"].max()
        wk_low = hist["Low"].min()
        short = "Bullish" if ltp > sma20 else "Bearish"
        medium = "Bullish" if ltp > sma50 else "Bearish"
        longterm = "Bullish" if ltp > sma200 else "Bearish"
        global_symbols = {
            "☃️S&P500":"^GSPC",
            "☃️Nasdaq":"^IXIC",
            "☃️Dow Jones":"^DJI",
            "🔔Vix":"^VIX",
            "💸Bitcoin":"BTC-USD",
            "💰Etherium":"ETH-USD",
            "🥇Gold":"GC=F",
            "🥈Silver":"SI=F",
            "🛢️Crude oil":"CL=F"
        }
        global_data = ""
        for name,ticker in global_symbols.items():
            try:
                g = yf.Ticker(ticker).history(period="2d")
                lastp = g["Close"].iloc[-1]
                prevp = g["Close"].iloc[-2]
                change = ((lastp-prevp)/prevp)*100
                global_data += f"{name}: {round(lastp,2)} ({round(change,2)}%)\n"
            except:
                global_data += f"{name}: Data NA\n"
        global_monitor = f"""
---------------------------------------------------------------
🚦🚦🚦🚦🌎Global Market Monitor🌎🚦🚦🚦🚦
---------------------------------------------------------------
{global_data}
"""
        indian_symbols = {
            "🦁Nifty50":"^NSEI",
            "🦁Banknifty":"^NSEBANK",
            "🦁Sensex":"^BSESN"
        }
        indian_data = ""
        for name,ticker in indian_symbols.items():
            try:
                i = yf.Ticker(ticker).history(period="2d")
                lastp = i["Close"].iloc[-1]
                prevp = i["Close"].iloc[-2]
                change = ((lastp-prevp)/prevp)*100
                indian_data += f"{name}: {round(lastp,2)} ({round(change,2)}%)\n"
            except:
                indian_data += f"{name}: Data NA\n"
        indian_monitor = f"""
---------------------------------------------------------------
🚦🚦🚦🚦🦁Indian Market Monitor🦁🚦🚦🚦🚦
---------------------------------------------------------------
{indian_data}
"""
        now = datetime.datetime.now()
        output_text = f"""
{DISCLAIMER_TEXT}
---------------------------------------------------------------
{SIGNATURE_TEXT}
---------------------------------------------------------------
💎Symbol: {symbol}
📆Time: {now}
---------------------------------------------------------------
🚦🚦🚦🚦💎About The Stock💎🚦🚦🚦🚦
---------------------------------------------------------------
✅Company Name: {info.get("longName")}
✅Sector: {info.get("sector")}
✅Industry: {info.get("industry")}
✅Country: {info.get("country")}
✅Website: {info.get("website")}
✅Business Summary:
{info.get("longBusinessSummary")}



---------------------------------------------------------------
🚦🚦🚦🚦🏆Fundamental Monitor🏆🚦🚦🚦🚦
---------------------------------------------------------------
🟢Market Cap: {info.get("marketCap")}
🟢Total Revenue: {info.get("totalRevenue")}
🟢Gross Profit: {info.get("grossProfits")}
⚫Net Income: {info.get("netIncomeToCommon")}
⚫Revenue Growth: {info.get("revenueGrowth")}
🟣Forward EPS: {info.get("forwardEps")}
🟣PE: {info.get("trailingPE")}
🟣EPS: {info.get("trailingEps")}
🟤Price to Book: {info.get("priceToBook")}
🟤Book Value: {info.get("bookValue")}
🔵Operating Margin: {info.get("operatingMargins")}
🔵Profit Margin: {info.get("profitMargins")}
🟡EBITDA: {info.get("ebitda")}
🟡EBITDA Margin: {info.get("ebitdaMargins")}
🔴Total Debt: {info.get("totalDebt")}
🔴Debt to Equity: {info.get("debtToEquity")}
🟠Total Cash: {info.get("totalCash")}



--------------------------------------------------------------- 
🚦🚦🚦🚦⚙️Technical Monitor⚙️🚦🚦🚦🚦
---------------------------------------------------------------
🧮LTP: {round(ltp,2)}
🔒Prev Close: {round(prev_close,2)}
🔓Open: {openp}
⏫High: {high}
⏬Low: {low}
⚖Volume: {volume}
📊SMA20: {round(sma20,2)}
📊SMA50: {round(sma50,2)}
📊SMA100: {round(sma100,2)}
📊SMA200: {round(sma200,2)}
📈52W High: {wk_high}
📉52W Low: {wk_low}
🎰RSI(14): {round(rsi,2)}
🎰Upper Bollinger Band: {round(bb_upper,2)}
🎰Lower Bollinger Band: {round(bb_lower,2)}
🎰VWAP: {round(vwap,2)}
🎰ATR: {round(atr,2)}
🎰Volatility: {round(volatility,4)}



--------------------------------------------------------------- 
🚦🚦🚦🚦🎯Trend Monitor🎯🚦🚦🚦🚦
---------------------------------------------------------------
⏰Short Term Trend: {short}
⏰Medium Term Trend: {medium}
⏰Long Term Trend: {longterm}


{indian_monitor}
{global_monitor}

---------------------------------------------------------------
💾Data Source: NSE / Yahoo / Other Screeners etc
---------------------------------------------------------------
🚦🚦🚦🚦☠️Warning☠️🚦🚦🚦🚦
---------------------------------------------------------------
This Stock Monitoring System is strictly for Educational, Informational and Fun purposes only.
This system only displays publicly available Market Data and Calculated Indicators derived from sources.
The Developer of this App is not Registered with SEBI as an Investment Adviser or Research Analyst.
Therefore, Please don't rely on the information provided here for making Investment or Trading decisions.
Investments in the Stock Market are subject to Market Risks, including the possible loss of principal.
Users are Strongly Advised to Conduct their Own Research (DYOR) and consult a SEBI Registered Investment Adviser or Financial Professional before making any Investment Decisions.
By using this App, you acknowledge that all Investment & Trading Decisions are taken at your Own Risk.
"""
        return output_text
# ------------------- RUN CLI OR STREAMLIT -------------------
if __name__=="__main__":
    import streamlit as st
    st.title("🐝 BuzyBeeStocks Stock Info App")
    symbol = st.text_input("Enter Stock Symbol (Example RELIANCE)")
    if st.button("Get Stock Info"):
        app_instance = BuzyBee()
        st.text(app_instance.get_stock_info(symbol))
