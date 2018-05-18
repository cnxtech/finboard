# finboard [![Build Status](https://travis-ci.org/Swalloow/finboard.svg?branch=master)](https://travis-ci.org/Swalloow/finboard) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/f853e1b3eaa24a0590b5a66245406616)](https://www.codacy.com/app/Swalloow/finboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Swalloow/finboard&amp;utm_campaign=Badge_Grade)
Collect financial features

# Architecture
![architecture](http://drive.google.com/uc?export=view&id=1djw9F_K1CHB_yClDNhLKeuJDATrcPudC)

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
