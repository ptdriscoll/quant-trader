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

def execute_order(trading_client, asset_type, ticker, side, price):
    """Submits order while logging the true cost, including real-world friction penalties."""
    
    if asset_type not in FEE_MODEL:
        raise ValueError(
            f'Unsupported asset type: {asset_type}'
        )
        
    model = FEE_MODEL[asset_type]    
    slippage_pct = model['slippage_pct']
    reg_fee = model.get('reg_fee_per_sell', 0)
    fee_pct = model.get('taker_fee_pct', 0)
    
    if asset_type == 'crypto':
        order_data = MarketOrderRequest(
            symbol=ticker,
            notional=100,
            side=side,
            time_in_force=TimeInForce.GTC
        )
    else:
        order_data = MarketOrderRequest(
            symbol=ticker,
            qty=1,
            side=side,
            time_in_force=TimeInForce.DAY
        )
        
    try:
        # Step 5: Friction Model calculations
        if side == OrderSide.BUY:
            # Realistically pays slightly more than the displayed ticker price due to the spread
            simulated_execution_price = price * (1 + slippage_pct + fee_pct)
            print(
                f'[{asset_type.upper()}] '
                f'BUY {ticker} | '
                f'Display: ${price:.2f} | '
                f'Simulated Fill: ${simulated_execution_price:.2f}'
            )
        else:
            # Receives slightly less when selling, and must pay regulatory micro-fees
            simulated_execution_price = (price * (1 - slippage_pct - fee_pct)) - reg_fee
            print(
                f'[{asset_type.upper()}] '
                f'SELL {ticker} | ' 
                f'Display: ${price:.2f} | ' 
                f'Simulated Fill: ${simulated_execution_price:.2f}'
            )
            
        trading_client.submit_order(order_data=order_data)
        print(f'    ✅ Order dispatched safely for {ticker}.')
        
    except Exception as e:
        print(f'    ❌ Execution failed for {ticker}: {e}')
