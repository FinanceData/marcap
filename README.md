# 데이터셋 - 시가총액 데이터 소개

<img width="80%" border="2" src="https://i.imgur.com/NeFOe4Y.png" >

* 한국거래소(KRX)에서 일자별 시가총액 순위 데이터
* 1995-05-02 ~ 2020-10-15 (25년간), 1천만건+ (CSV)

#### 2018-2020 [FinanceData.KR](http://facebook.com/financedata)

## 시가총액
시가총액(時價總額, market capitalization)은 주식 값의 총합 즉, `주가 X 발행주식수`이며, 간단히 특정 회사의 경제적 크기를 말합니다.

현재(2019년 2분기), 삼성전자의 시가총액은 약 261조원, 한국전력은 약 16조원입니다. 단순하게 비교해서 삼성전자는 한국전력보다 약 16배 크다고 이야기 할 수 있습니다.

거래소 홈페이지에 공개된 시가총액 데이터를 활용하여 상장기업의 시가총액을 간단하게 분석하고 시각화 해봅니다.


## 상장회사 시가총액 데이터

상장회사에 대한 정보는 [한국거래소](http://marketdata.krx.co.kr) 홈페이지에서 손쉽게 얻을 수 있습니다. 아래 URL은 특정 날짜의 시가총액 상위 종목을 조회하는 화면입니다. 상장 종목 전체의 시가총액 순위를 얻을 수 있습니다. 덧붙여 중요한 사실은 바로 특정 시점의 모든 종목에 대한 종목과 종목 코드를 얻을 수 있다는 점입니다. 다시 말해, 오늘 날짜로 검색하면 현재 시장에서 거래되는 모든 종목의 종목 코드, 종목명, 시가총액 정보를 얻을 수 있습니다.

http://marketdata.krx.co.kr/contents/MKD/04/0406/04060100/MKD04060100.jsp

위 링크로 바로 접근하거나  메뉴에서 다음과 같은 순서로접근할 수도 있습니다.

시장정보 → 주식 → 순위정보 → 시가총액 상/하위

<img src="http://i.imgur.com/sd7snXg.png" >
    

시장 구분과 업종 구분은 `전체`로 하고 조회 일자는 현재 날짜로 하거나 조회하고자 하는 년도의 날짜를 입력합니다. `CSV`를 선택하면 `data.csv`로 데이터를 내려받을 수 있습니다. 이 데이터를 정리하고 년도 별로 묶은 것이 `시가총액(marcap) 데이터셋` 입니다.



## 시가총액(marcap) 데이터셋의 구성

시가총액(marcap) 데이터셋은 1995-05-02 ~ 2019-03-27일까지 25년간 일자별, 17개 컬럼, 1천만건+ 데이터 입니다.
압축하지 않은 상태에서  `1.3G` 분량 입니다.

https://financedata.github.io/marcap/

* 컬럼: 17개
* 건수: 10,946,427 건(row)
* 크기: 1.3G+


#### 컬럼 구성 
Date (날짜)를 인덱스(DatetimeIndex)로 포함하고 있으며, 컬럼 구성은 다음과 같습니다.

* Date : 날짜 (DatetimeIndex)
* Code : 종목코드
* Name : 종목이름 
* Open : 시가
* High : 고가
* Low : 저가
* Close : 종가
* Volume : 거래량
* Amount : 거래대금
* Changes : 전일대비
* ChagesRatio : 전일비
* Marcap : 시가총액(백만원)
* Stocks : 상장주식수
* MarcapRatio : 시가총액비중(%)
* ForeignShares : 외국인 보유주식수
* ForeignRatio : 외국인 지분율(%)
* Rank: 시가총액 순위 (당일)

## 데이터 가져오기
다음과 같이 단 한 줄의 명령으로 데이터를 가져올 수 있습니다.

git 명령으로 깃허브의 저장소를 복제(clone)합니다. 데이터와 데이터를 읽는데 도움이 되는 간단한 파이썬 유틸리티 함수가 포함되어 있습니다.



```
git clone "https://github.com/FinanceData/marcap.git" marcap
```

데이터는 ./marcap/data 디렉토리에 있으며 년도별 CSV 파일로 구성되어 있습니다. 개별 파일은 .gz으로 압축되어 있습니다.


## 유틸리티 함수

marcap 시가총액 데이터셋에는 데이터를 날짜별로 혹은 기간과 특정 종목을 지정하여 손쉽게 읽기 위한 유틸함수가 있습니다. <br>
다음과 같이 import 하여 사용합니다.

```python 
from marcap import marcap_data
```

### marcap_data(start, end=None, code=None)
지정한 기간 데이터 읽어옵니다. 종목코드(code)를 지정하면 해당 종목에 대한 데이터를 지정한 기간만큼 읽어 옵니다. 거래량(volume)이 0인 행(row)는 제거하고 반환합니다.


간단한 사용 예제를 살펴보면,


```python
# 특정 날짜를 지정하여 읽기
df = marcap_data('2019-5-2')

# 기간을 지정하여 읽기 (2018년 1년간 전종목)
df = marcap_data('2018-01-01', '2018-12-31')

# 기간을 지정하여, 특정 종목 읽기 (2018년 1년간 특정 종목)
df = marcap_data('2018-01-01', '2018-12-31', code='005930')

# 특정 종목 특정 하루 ()
df = marcap_data('2018-12-28', code='005930')

# 24년간 데이터 모두 읽기
df = marcap_data('1995-05-02', '2020-03-27')
```

## 활용

지난 24년간 개별 종목의 가격 데이터(시가,고가,종가,저가,거래량, 전일대비등락) 뿐만 아니라 외국인 지분율을 분석하거나

<img src="https://i.imgur.com/Z2uUZ2y.png" >

섹터별 시가총액을 분석하는데도 사용할 수 있습니다.

<img src="https://i.imgur.com/Kp94vvl.png" >



보다 상세한 내용은 [튜토리얼 문서](https://nbviewer.jupyter.org/github/FinanceData/marcap/blob/master/marcap-tutorial.ipynb)를 참고하십시오. [구글 Colab에서 바로 실행](https://colab.research.google.com/github/FinanceData/marcap/blob/master/marcap-tutorial.ipynb)해 볼 수 있습니다


## Last Updated
2020-10-16


#### 2018-2020 [FinanceData.KR]()
