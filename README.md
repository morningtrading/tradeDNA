# TradeDNA Strategy

TradeDNA is a dual-direction Freqtrade strategy built around:

- EMA20(high) / EMA20(low) channel structure
- Heiken Ashi trend confirmation
- RSI momentum filter
- Elephant bar impulse detection
- Pullback entries
- Dynamic ROI
- Custom stoploss
- Hyperoptable parameters

This repository includes:

- Strategy file
- Documentation
- Example configs
- Scripts for backtesting and hyperopt
- Tools for data and pairlist management
- .env-example for Hyperliquid credentials

## Installation

Clone the repo:

    git clone https://github.com/YOUR_USERNAME/TradeDNA.git

Copy the strategy into your Freqtrade user_data:

    cp strategies/TradeDNA.py ~/freqtrade/user_data/strategies/

## Backtesting

    freqtrade backtesting --strategy TradeDNA

## Hyperopt

    freqtrade hyperopt --strategy TradeDNA --spaces buy sell roi stoploss

## Documentation

See the docs/ folder for more details.

## License

MIT License.
