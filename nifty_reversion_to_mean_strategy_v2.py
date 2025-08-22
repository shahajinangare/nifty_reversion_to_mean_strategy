import pandas as pd 
import numpy as np 
from collections import defaultdict 
import streamlit as st

st.header('Nifty “Reversion to Mean” Strategy')

# ---- CONFIGURATION ---- # 
LOT_SIZE_CASH = int(st.sidebar.text_input('LOT SIZE CASH', '5000'))    # Rs per lot per buy trigger 
PROFIT_TARGET =int(st.sidebar.text_input('PROFIT TARGET', '5'))/100    # 5% above average buy price to trigger sell 
st.sidebar.markdown("----")
st.sidebar.markdown("")
ref_price_1=st.sidebar.text_input('REF PRICE 1', '4.13')
ref_price_2=st.sidebar.text_input('REF PRICE 1', '8.26')
ref_price_3=st.sidebar.text_input('REF PRICE 1', '12.39')

# -- Helper: Calculate trigger prices -- # 
def get_triggers(ref_price): 
    return [ 
        round(ref_price * (1 - (float(ref_price_1)/100)), 2),   # 4.13% 
        round(ref_price * (1 - (float(ref_price_2)/100)), 2),   # 8.26% 
        round(ref_price * (1 - (float(ref_price_3)/100)), 2)    # 12.39% 
    ] 
 
# ---- STRATEGY LOGIC ---- # 
def run_nifty_shop(prices_df, lot_size_cash=LOT_SIZE_CASH, profit_target=PROFIT_TARGET): 
    trade_log = [] 
    positions = defaultdict(list)         # {stock: [ {"buy_price": X, "date": date, "shares": N}, ... ]} 
    triggers_used = defaultdict(lambda: [False, False, False]) # {stock: [bool, bool, bool] per year} 
    reference_prices = {}                 # {stock: ref_price per year} 
    prev_year = None 
 
    for day, row in prices_df.iterrows(): 
        year = day.year 
        if (prev_year is None) or (year != prev_year): 
            # Reset for a new year 
            triggers_used = defaultdict(lambda: [False, False, False]) 
            # Set yearly reference prices 
            reference_prices = {stock: row[stock] for stock in prices_df.columns if not np.isnan(row[stock])} 
            prev_year = year 
 
        # --- BUYING LOGIC --- # 
        for stock in prices_df.columns: 
            current_price = row[stock] 
            if np.isnan(current_price): 
                continue 
            ref_price = reference_prices.get(stock) 
            if not ref_price: 
                continue 
            triggers = get_triggers(ref_price) 
            # One lot per trigger per year 
            for idx, trig_price in enumerate(triggers): 
                if (not triggers_used[stock][idx]) and (current_price <= trig_price): 
                    shares = int(lot_size_cash // current_price) 
                    if shares == 0: 
                        continue 
                    positions[stock].append( {'buy_price': current_price, 'date': day, 'shares': shares} ) 
                    trade_log.append({"date": day, "stock": stock, "action": "BUY", "price": current_price, "shares": shares, "level": f"{int((idx+1)*4.13)}%"}) 
                    triggers_used[stock][idx] = True 
                    break  # Don't buy the next (deeper) level on same day 
 
        # --- SELLING LOGIC --- # 
        # At end of day (simulate at 3:20 PM), check all holdings for >5% above avg buy price 
        sell_candidates = [] 
        for stock, buys in positions.items(): 
            if not buys: 
                continue 
            # Compute (overall) average buy price for current holdings 
            total_shares = sum(b['shares'] for b in buys) 
            if total_shares == 0: 
                continue 
            avg_buy_price = sum(b['buy_price'] * b['shares'] for b in buys) / total_shares 
            # Is current price >5% above avg buy? 
            current_price = row[stock] 
            if current_price / avg_buy_price > (1 + profit_target): 
                sell_candidates.append( (stock, current_price, avg_buy_price) ) 
 
        # Only sell 1 lot (from most profitable position above 5%), per day! 
        if sell_candidates: 
            # Choose the one with highest percentage gain 
            best_stock, best_price, best_avg = max( 
                sell_candidates, key=lambda x: (x[1]/x[2] - 1) 
            ) 
            # Sell one lot (i.e., min number of shares in any outstanding lot) 
            total_shares = sum(b['shares'] for b in positions[best_stock]) 
            # Find smallest lot's share count (ensure strict 1-lot-out rule) 
            min_lot = min(b['shares'] for b in positions[best_stock]) 
            to_sell = min_lot 
 
            # Remove from positions: subtract sell shares from earliest buy lots 
            shares_sold = 0 
            for b in positions[best_stock]: 
                if b['shares'] >= to_sell: 
                    b['shares'] -= to_sell 
                    break 
                else: 
                    to_sell -= b['shares'] 
                    b['shares'] = 0 
            # Optionally, remove lots with 0 shares 
            positions[best_stock] = [b for b in positions[best_stock] if b['shares'] > 0] 
 
            trade_log.append({"date":  day,  "stock":  best_stock,  "action":  "SELL",  "price":  best_price,  "shares": min_lot, 
                              "reason": f">5% above avg buy ({round((best_price/best_avg-1)*100,1)}%)"}) 
 
    return pd.DataFrame(trade_log) 

def handle_click():
    # st.write("Callback function executed!")
    # --------------------------------------------- 
    # Example usage: 
    # Suppose you have 'prices_df' loaded: rows = dates, columns = stock symbols 
    prices_df = pd.read_csv('./nifty50_closing_prices.csv', index_col=0, parse_dates=True) 
    trades = run_nifty_shop(prices_df) 
    st.write(trades)
    # print(trades) 
    # ---------------------------------------------

st.button("Click me! Show Result", on_click=handle_click)
# Add a horizontal line below the content
st.markdown("---")
