from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest

FEE_MODEL = {
    'equity': {
        'slippage_pct': 0.0002,
        'reg_fee_per_sell': 0.00002
    },
    'crypto': {
        'slippage_pct': 0.0015,  # Higher slippage for crypto market impact
        'maker_fee_pct': 0.0010, # Fee when providing liquidity (limit orders)
        'taker_fee_pct': 0.0020  # Fee when taking liquidity (market orders)
    }
}

def execute_order(asset_type, ticker, side, price):
    """Submits order while logging the true cost, including real-world friction penalties."""
    
    model = FEE_MODEL[asset_type]
    slippage_pct = model['slippage_pct']
    reg_fee = model.get('reg_fee_per_sell', 0)
    
    if asset_type == 'crypto':
        tif = TimeInForce.GTC
    else:
        tif = TimeInForce.DAY
        
    try:
        # Step 5: Friction Model calculations
        if side == OrderSide.BUY:
            # Realistically pays slightly more than the displayed ticker price due to the spread
            simulated_execution_price = price * (1 + slippage_pct)
            print(f' Buying {ticker} | Display: ${price:.2f} | Simulated Fill: ${simulated_execution_price:.2f}')
        else:
            # Receives slightly less when selling, and must pay regulatory micro-fees
            simulated_execution_price = (price * (1 - slippage_pct)) - reg_fee
            print(f' Selling {ticker} | Display: ${price:.2f} | Simulated Fill: ${simulated_execution_price:.2f}')
            
        order_data = MarketOrderRequest(
            symbol=ticker,
            qty=1,
            side=side,
            time_in_force=tif
        )
        trading_client.submit_order(order_data=order_data)
        print(f'    ✅ Order dispatched safely for {ticker}.')
        
    except Exception as e:
        print(f'    ❌ Execution failed for {ticker}: {e}')
