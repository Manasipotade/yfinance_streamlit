import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
from io import BytesIO


# Use yfinance with pandas_datareader
yf.pdr_override()

# Symbols for downloading data
symbols = ['AARTIIND.NS','ABB.NS','ABBOTINDIA.NS','ABCAPITAL.NS','ABFRL.NS','ACC.NS','ADANIENT.NS',
           'ADANIPORTS.NS','ALKEM.NS','AMBUJACEM.NS','APOLLOHOSP.NS','APOLLOTYRE.NS','ASHOKLEY.NS',
           'ASIANPAINT.NS','ASTRAL.NS','ATUL.NS','AUBANK.NS','AUROPHARMA.NS','AXISBANK.NS','BAJAJ-AUTO.NS',
           'BAJAJFINSV.NS','BAJFINANCE.NS','BALKRISIND.NS','BALRAMCHIN.NS','BANDHANBNK.NS','BANKBARODA.NS',
           'BATAINDIA.NS','BEL.NS','BERGEPAINT.NS','BHARATFORG.NS','BHARTIARTL.NS','BHEL.NS','BIOCON.NS',
           'BOSCHLTD.NS','BPCL.NS','BRITANNIA.NS','BSOFT.NS','CANBK.NS','CANFINHOME.NS','CHAMBLFERT.NS',
           'CHOLAFIN.NS','CIPLA.NS','COALINDIA.NS','COFORGE.NS','COLPAL.NS','CONCOR.NS','COROMANDEL.NS',
           'CROMPTON.NS','CUB.NS','CUMMINSIND.NS','DABUR.NS','DALBHARAT.NS','DEEPAKNTR.NS','DIVISLAB.NS',
           'DIXON.NS','DLF.NS','DRREDDY.NS','EICHERMOT.NS','ESCORTS.NS','EXIDEIND.NS','FEDERALBNK.NS',
           'GAIL.NS','GLENMARK.NS','GMRINFRA.NS','GNFC.NS','GODREJCP.NS','GODREJPROP.NS','GRANULES.NS',
           'GRASIM.NS','GUJGASLTD.NS','HAL.NS','HAVELLS.NS','HCLTECH.NS','HDFCAMC.NS','HDFCBANK.NS',
           'HDFCLIFE.NS','HEROMOTOCO.NS','HINDALCO.NS','HINDCOPPER.NS','HINDPETRO.NS','HINDUNILVR.NS',
           'ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS','IDEA.NS','IDFC.NS','IDFCFIRSTB.NS','IEX.NS',
           'IGL.NS','INDHOTEL.NS','INDIACEM.NS','INDIAMART.NS','INDIGO.NS','INDUSINDBK.NS','INDUSTOWER.NS',
           'INFY.NS','IOC.NS','IPCALAB.NS','IRCTC.NS','ITC.NS','JINDALSTEL.NS','JKCEMENT.NS','JSWSTEEL.NS',
           'JUBLFOOD.NS','KOTAKBANK.NS','LALPATHLAB.NS','LAURUSLABS.NS','LICHSGFIN.NS','LT.NS','LTF.NS',
           'LTIM.NS','LTTS.NS','LUPIN.NS','M&M.NS','M&MFIN.NS','MANAPPURAM.NS','MARICO.NS','MARUTI.NS',
           'MCDOWELL-N.NS','MCX.NS','METROPOLIS.NS','MFSL.NS','MGL.NS','MOTHERSON.NS','MPHASIS.NS','MRF.NS',
           'MUTHOOTFIN.NS','NATIONALUM.NS','NAUKRI.NS','NAVINFLUOR.NS','NESTLEIND.NS','NMDC.NS','NTPC.NS',
           'OBEROIRLTY.NS','OFSS.NS','ONGC.NS','PAGEIND.NS','PEL.NS','PERSISTENT.NS','PETRONET.NS','PFC.NS',
           'PIDILITIND.NS','PIIND.NS','PNB.NS','POLYCAB.NS','POWERGRID.NS','PVRINOX.NS','RAMCOCEM.NS',
           'RBLBANK.NS','RECLTD.NS','RELIANCE.NS','SAIL.NS','SBICARD.NS','SBILIFE.NS','SBIN.NS','SHREECEM.NS',
           'SHRIRAMFIN.NS','SIEMENS.NS','SRF.NS','SUNPHARMA.NS','SUNTV.NS','SYNGENE.NS','TATACHEM.NS',
           'TATACOMM.NS','TATACONSUM.NS','TATAMOTORS.NS','TATAPOWER.NS','TATASTEEL.NS','TCS.NS','TECHM.NS',
           'TITAN.NS','TORNTPHARM.NS','TRENT.NS','TVSMOTOR.NS','UBL.NS','ULTRACEMCO.NS','UPL.NS','VEDL.NS',
           'VOLTAS.NS','WIPRO.NS','ZEEL.NS','ZYDUSLIFE.NS']

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