import datetime as dt

PROJECT_NAME = 'Stock Smart'
MENU = [
    'Home',
    'Choose company',
    'View raw data',
    'View stock price graphs',
    'Calculate results',
    'Show history',
    'About'
]
stks = {
    'Facebook':'FB',
    'Apple':'AAPL',
    'Tesla':'TSLA',
    'Amazon':'AMZN',
    'Google':'GOOG',
    'Microsoft Corporation':'MSFT',
    'Tata Motors Limited':'TTM',
    'Netflix, Inc.':'NFLX',
    'NVIDIA Corporation':'NVDA',
    'Wipro Limited':'WIPRO.NS',
    'Dogecoin USD':'DOGE-USD',
    'EthereumClassic USD':'ETC-USD',
    'BitcoinCash USD':'BCH-USD',
    'QuantumScape Corporation':'QS',
    'Virgin Galactic Holdings, Inc.':'SPCE',
    'Dogecoin INR':'DOGE-INR',
    'The Toro Company':'TTC',
    'Churchill Capital Corp IV':'CCIV',
    'Plug Power Inc.':'PLUG',
    'Singapore Telecommunications Limited':'Z74.SI',
    'FuelCell Energy, Inc.':'FCEL',
    }
start = dt.datetime(2013, 1, 1)
end = dt.datetime.now()
