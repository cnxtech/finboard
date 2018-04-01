# Rogers-Collector
Collect financial features

## Deploy to AWS Lambda

```
# create lambda function
python manager.py create

# update lambda function
python manager.py update

# invoke lambda function
python manager.py invoke --payload=[target_name]
```

## Schema

```
crypto (exchange: PK, date: SK)
 - name (화폐) : btc, eth, xrp
 - exchange (거래소) : bithumb, coinone, korbit
 - price (가격)
 - volume (거래량)
 - date (날짜) : "%Y-%m-%d %H:%M:%S"
```
```
market (type: PK, date: SK)
 - name (대상) : WTI, GSOIL, WGOLD, LGOLD, USD, JPY, EUR, CNY
 - price (가격)
 - status (변화)
 - date (날짜) : "%Y-%m-%d %H:%M:%S"
```
```
index (type: PK, date: SK)
 - name (대상) : KOSPI, KOSDAQ, ...
 - price (가격)
 - status (변화)
 - rate (비율)
 - date (날짜) : "%Y-%m-%d %H:%M:%S"
```
```
stock (name: PK, date: SK)
 - name (종목명)
 - close (종가)
 - open (시가)
 - high (고가)
 - low (저가)
 - diff (변화)
 - volume (거래량)
 - date (날짜) : "%Y-%m-%d %H:%M:%S"
```