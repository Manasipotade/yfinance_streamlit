import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
from io import BytesIO


# Use yfinance with pandas_datareader
yf.pdr_override()

# Lists of stocks for each category

fno_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']  # Add more FNO stocks
nifty50_stocks = ['INFY.NS', 'HDFC.NS', 'ITC.NS']  # Add more Nifty 50 stocks
indices = ['^NSEI', '^BSESN']  # Nifty 50 and Sensex indices


# Function to fetch stock data
def fetch_stock_data(symbols, interval, period):
    stock_final = pd.DataFrame()
    for symbol in symbols:
        try:
            stock = yf.download(symbol, progress=False, period=period, interval=interval)
            if not stock.empty:
                stock['Name'] = symbol
                stock_final = pd.concat([stock_final, stock], sort=False)
        except Exception as e:
            print(f"Error downloading data for {symbol}: {e}")
    return stock_final

# Streamlit app
def main():
    st.title('Stock Data Downloader')
    
    # Radio buttons for stock category selection
    stock_category = st.radio(
        "Select stock category",
        ('FNO Stocks', 'Nifty 50', 'Indices')
    )
    
    # Update symbols list based on selected category
    if stock_category == 'FNO Stocks':
        symbols = fno_stocks
    elif stock_category == 'Nifty 50':
        symbols = nifty50_stocks
    else:
        symbols = indices
    
    # Display selected symbols
    st.write(f"Selected category: {stock_category}")
    st.write("List of selected stock symbols:")
    st.text_area('Symbols', ', '.join(symbols), height=150)  
    
    # Input fields
    interval = st.text_input('Enter Time Interval (e.g., 1m, 2m, 1h, 1d, 1wk, 1mo)', '1d')
    period = st.text_input('Enter Time Period (e.g., 1d, 5d, 1mo, 3mo, 1y)', '1mo')

    # Button to fetch data
    
    if st.button('Fetch Data'):
        with st.spinner('Fetching data...'):
            stock_data = fetch_stock_data(symbols, interval, period)
            if not stock_data.empty:
                st.success('Data fetched successfully!')
                st.dataframe(stock_data)
                
                # Save to Excel in memory
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                excel_filename = f'Stock_Data_{timestamp}.xlsx'
                towrite = BytesIO()
                stock_data.to_excel(towrite, index=True, engine='openpyxl')
                towrite.seek(0)

                # Download button
                st.download_button(label='Download Excel file', data=towrite, file_name=excel_filename, mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                st.error('No data fetched. Please check your inputs.')

if __name__ == '__main__':
    main()
