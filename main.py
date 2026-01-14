import json
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
from openai import OpenAI

# -----------------------------
# Load API Key securely
# -----------------------------
with open("API_KEY", "r") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

# -----------------------------
# Stock utility functions
# -----------------------------
def getStockPrice(ticker):
    return str(yf.Ticker(ticker).history(period="1y").iloc[-1].Close)

def calculateSMA(ticker, window):
    data = yf.Ticker(ticker).history(period="1y").Close
    return str(data.rolling(window=window).mean().iloc[-1])

def calculateEMA(ticker, window):
    data = yf.Ticker(ticker).history(period="1y").Close
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])

def calculateRSI(ticker):
    data = yf.Ticker(ticker).history(period="1y").Close
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=13, adjust=False).mean()
    avg_loss = loss.ewm(com=13, adjust=False).mean()
    rs = avg_gain / avg_loss
    return str(100 - (100 / (1 + rs))).split("\n")[-1]

def calculateMACD(ticker):
    data = yf.Ticker(ticker).history(period="1y").Close
    ema12 = data.ewm(span=12, adjust=False).mean()
    ema26 = data.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    return f"MACD: {macd.iloc[-1]}, Signal: {signal.iloc[-1]}, Histogram: {histogram.iloc[-1]}"

def plotStockPrice(ticker):
    data = yf.Ticker(ticker).history(period="1y")
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.Close)
    plt.title(f"{ticker} Stock Price (1Y)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.savefig("stock.png")
    plt.close()

# -----------------------------
# Tool definitions (NEW FORMAT)
# -----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "getStockPrice",
            "description": "Get latest stock price",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"}
                },
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculateSMA",
            "description": "Calculate SMA",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"},
                    "window": {"type": "integer"}
                },
                "required": ["ticker", "window"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculateEMA",
            "description": "Calculate EMA",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"},
                    "window": {"type": "integer"}
                },
                "required": ["ticker", "window"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculateRSI",
            "description": "Calculate RSI",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"}
                },
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculateMACD",
            "description": "Calculate MACD",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"}
                },
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "plotStockPrice",
            "description": "Plot stock price (1Y)",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"}
                },
                "required": ["ticker"]
            }
        }
    }
]

available_functions = {
    "getStockPrice": getStockPrice,
    "calculateSMA": calculateSMA,
    "calculateEMA": calculateEMA,
    "calculateRSI": calculateRSI,
    "calculateMACD": calculateMACD,
    "plotStockPrice": plotStockPrice,
}

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("📈 StockSage – Stock Analysis Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Ask about a stock:")

if user_input:
    try:
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            result = available_functions[fn_name](**fn_args)

            if fn_name == "plotStockPrice":
                st.image("stock.png")
            else:
                st.session_state.messages.append(msg)
                st.session_state.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

                final_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )

                answer = final_response.choices[0].message.content
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.write(msg.content)
            st.session_state.messages.append({"role": "assistant", "content": msg.content})

    except Exception as e:
        st.error(f"Error: {e}")
