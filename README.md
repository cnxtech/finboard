# Finboard [![Build Status](https://travis-ci.org/Swalloow/finboard.svg?branch=master)](https://travis-ci.org/Swalloow/finboard) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/f853e1b3eaa24a0590b5a66245406616)](https://www.codacy.com/app/Swalloow/finboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Swalloow/finboard&amp;utm_campaign=Badge_Grade)

- 금융 정보를 수집하고 저장하며 대시보드를 통해 시각화
- 수집 데이터: 가상화폐, 세계증시, 국내증시, 파생상품
- 배치 작업은 `AWS Lambda + CloudWatch` 스케줄러를 활용
- 대시보드는 `Grafana`를 활용, 시계열 데이터베이스로 `ElasticSearch` 활용
- `lambda streamer`를 통해 DynamoDB에서 ElasticSearch로 실시간 업데이트
- AWS 프리티어 한도 내에서 적용 가능

# Architecture
![architecture](http://drive.google.com/uc?export=view&id=1Dt0dNppLMPp1hAWrj8y8au0Y5QO-DUHN)

# Dashboard
![dashboard](http://drive.google.com/uc?export=view&id=12CbBgB9mZptB6SPEa2m_dRBXUpnbrPw1)

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
// 가상화폐 (빗썸, 코인원, 코빗)
crypto (exchange: PK, date: SK)
 - name (화폐) : btc, eth, xrp
 - exchange (거래소) : bithumb, coinone, korbit
 - price (가격)
 - volume (거래량)
 - date (날짜) : "%Y-%m-%d %H:%M:%S"
```
```
// 상품 시장 (유가, 금, 환율)
market (type: PK, date: SK)
 - name (대상) : WTI, GSOIL, WGOLD, LGOLD, USD, JPY, EUR, CNY
 - price (가격)
 - status (변화)
 - date (날짜) : "%Y-%m-%d %H:%M:%S"
```
```
// 세계 증시 (한국, 미국, 유럽, 중국, 일본, 인도)
index (type: PK, date: SK)
 - name (대상) : KOSPI, KOSDAQ, ...
 - price (가격)
 - status (변화)
 - rate (비율)
 - date (날짜) : "%Y-%m-%d %H:%M:%S"
```
```
// 코스피, 코스닥 일봉
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
```
// 코스피, 코스닥 정보
code (code: PK)
- code (종목코드)
- name (회사명)
- market (상장마켓) : kospi, kosdaq, konex
- industry (업종)
- product (주요제품)
- opening_date (상장일)
- closing_month (결산월)
- ceo (대표자명)
- homepage (홈페이지)
- local (지역)
```
