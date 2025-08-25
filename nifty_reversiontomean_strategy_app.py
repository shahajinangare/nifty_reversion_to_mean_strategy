import yfinance as yf
from nifty.service import ClosingPricesService
from nifty.strategy.reversiontomean import ReversionToMean
import streamlit as st

st.header('Nifty “Reversion to Mean” Strategy')

if "show_section" not in st.session_state:
    st.session_state.show_section = "None"

col1, col2 = st.columns(2)
with col1:
    if st.button("Click me! Show Result"):
        st.session_state.show_section = "A"
# with col2:
#     if st.button("Show Section B"):
#         st.session_state.show_section = "B"

# ---- CONFIGURATION ---- # 
LOT_SIZE_CASH = int(st.sidebar.text_input('LOT SIZE CASH', '5000'))    # Rs per lot per buy trigger 
PROFIT_TARGET =int(st.sidebar.text_input('PROFIT TARGET', '5'))/100    # 5% above average buy price to trigger sell 
st.sidebar.markdown("----")
st.sidebar.markdown("")
ref_price_1=st.sidebar.text_input('REF PRICE 1', '4.13')
ref_price_2=st.sidebar.text_input('REF PRICE 1', '8.26')
ref_price_3=st.sidebar.text_input('REF PRICE 1', '12.39')

def handle_click():
    # st.write("Callback function executed!")
    # --------------------------------------------- 
    # Example usage: 
    # Suppose you have 'prices_df' loaded: rows = dates, columns = stock symbols 
    # prices_df = pd.read_csv('./nifty50_closing_prices.csv', index_col=0, parse_dates=True) 
    prices_df=ClosingPricesService.get_nifty50_closing_price();
    st.write(prices_df)
    trades =ReversionToMean.run_nifty_shop(prices_df,ref_price_1,ref_price_2,ref_price_3,lot_size_cash=LOT_SIZE_CASH, profit_target=PROFIT_TARGET) 
    st.write(trades)
    # print(trades) 
    # ---------------------------------------------

# st.button("Click me! Show Result", on_click=handle_click)
# Add a horizontal line below the content

if st.session_state.show_section == "A":
    handle_click()