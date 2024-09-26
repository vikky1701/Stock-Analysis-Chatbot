# Stock-Analysis-Chatbot

Welcome to the **Stock-Analysis-Chatbot** project! This application is designed to assist users in analyzing stock data by providing functionalities such as fetching stock prices, calculating technical indicators, and visualizing stock performance over the past year.

## Features

- Get the latest stock price for any company.
- Calculate Simple Moving Average (SMA) and Exponential Moving Average (EMA).
- Compute Relative Strength Index (RSI) and Moving Average Convergence Divergence (MACD).
- Visualize stock price trends using plots.

## Technologies Used

- Python
- Streamlit
- OpenAI API
- yFinance
- Matplotlib
- Pandas
- NumPy

## Prerequisites

Ensure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

## To Run This Project
1. clone this project on your local machine,
```
git clone https://github.com/vikky1701/Stock-Analysis-Chatbot.git
```
2. Create a file named API_KEY in the project directory and add your OpenAI API key to this file.
```
   API_KEY
```
3. create a virtual environment inside Stock-Analysis-Chatbot folder,
```
python3 -m venv venv
```
3. activate virtual environment
```
source venv/bin/activate
```
4. install project dependencies from requirements.txt,
```
pip install -r requirements.txt
```
5. run project on your local machine,
```
streamlit run main.py
```

  
