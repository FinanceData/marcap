# 시가총액 데이터셋(marcap)

<img src="https://i.imgur.com/b9t5FAA.png?1" width="60%">

* 한국거래소(KRX)에서 일자별 시가총액 순위 데이터
* 1995-05-02 ~ 2020-12-31 (26년간), 1천만건 이상

## Quick Start

```bash
git clone "https://github.com/FinanceData/marcap.git" marcap
```

```python 
from marcap import marcap_data

# 특정 날짜 전종목
df = marcap_data('2021-01-21') 

# 특정 기간 전종목
df = marcap_data('2020-01-01', '2020-12-31') 

# 특정 기간 단일 종목
df = marcap_data('2021-01-01', '2021-01-31', code='005930') 
```

## 시가총액
시가총액(時價總額, market capitalization)은 주식 값의 총합 즉, `주가 X 발행주식수`이며, 간단히 특정 회사의 경제적 크기를 말합니다.

현재(2019년 2분기), 삼성전자의 시가총액은 약 261조원, 한국전력은 약 16조원입니다. 단순하게 비교해서 삼성전자는 한국전력보다 약 16배 크다고 이야기 할 수 있습니다.

거래소 홈페이지에 공개된 시가총액 데이터를 활용하여 상장기업의 시가총액을 간단하게 분석하고 시각화 해봅니다.



## 상장종목 시가총액 데이터
상장종목에 대한 가격과 시가총액 데이터는 [한국거래소](http://marketdata.krx.co.kr) 페이지에서 손쉽게 얻을 수 있습니다. 

http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101

상장 종목 전체의 가격 데이터와 시가총액 순위를 얻을 수 있습니다. 덧붙여 중요한 사실은 바로 특정 시점의 모든 종목에 대한 종목과 종목 코드를 얻을 수 있다는 점도 활용할 수 있습니다. 다시 말해, 오늘 날짜로 검색하면 현재 시장에서 거래되는 모든 종목의 종목 코드, 종목명, 시가총액 정보를 얻을 수 있습니다.

위 링크로 바로 접근하거나  메뉴에서 다음과 같은 순서로접근할 수도 있습니다.

정보데이터시스템 → 주식 → 종목시세 → 전종목시세

<img src="https://i.imgur.com/PwSvcBV.png" width="80%" >
    

시장 구분과 업종 구분은 `전체`로 하고 조회 일자는 현재 날짜로 하거나 조회하고자 하는 년도의 날짜를 입력합니다. 오른쪽 상단 다운로드 버튼을 눌러 CSV 혹은 엑셀 파일로 다운로드할 수 있습니다. 이 데이터를 정리하고 년도 별로 묶은 것이 `시가총액(marcap) 데이터셋` 입니다.



## 시가총액(marcap) 데이터셋의 구성

시가총액(marcap) 데이터셋은 1995-05-02 ~ 2020-12-31 (25년간)일자별, 18개 컬럼, 1천만건 데이터 입니다. 압축하지 않은 상태에서  약 '1.6G' 분량 입니다.

**github 저장소에 현재 날짜 데이터까지 매일 자동 업데이트 됩니다.** 
따라서 git 저장소를 pull 하시면 매일 전종목 가격 데이터를 업데이트 하실 수 있습니다. 

https://financedata.github.io/marcap/

* 컬럼: 18개
* 건수: 11,099,879 건(row)
* 크기: 1.6G


#### 컬럼 구성(18개)
Date (날짜)를 인덱스(DatetimeIndex)로 포함하고 있으며, 컬럼 구성은 다음과 같습니다.

* Date : 날짜 (DatetimeIndex)
* Rank: 시가총액 순위 (당일)
* Code : 종목코드
* Name : 종명이름 
* Open : 시가
* High : 고가
* Low : 저가
* Close : 종가
* Volume : 거래량
* Amount : 거래대금
* Changes : 전일대비
* ChangeCode: 등락 기호
* ChagesRatio : 전일대비 등락률
* Marcap : 시가총액(백만원)
* Stocks : 상장주식수
* MarketId : 시장기호	
* Market : 시장
* Dept : 부서(한국거래소)



## 데이터 가져오기
다음과 같이 단 한 줄의 명령으로 데이터를 가져올 수 있습니다.

git 명령으로 깃허브의 저장소를 복제(clone)합니다. 데이터와 데이터를 읽는데 도움이 되는 간단한 파이썬 유틸리티 함수가 포함되어 있습니다.

```bash
git clone "https://github.com/FinanceData/marcap.git" marcap
```

데이터는 ./marcap/data 디렉토리에 있으며 년도별 CSV 파일로 구성되어 있습니다. 개별 파일은 .gz으로 압축되어 있습니다.


## 유틸리티 함수

marcap 시가총액 데이터셋에는 데이터를 날짜별로 혹은 기간과 특정 종목을 지정하여 손쉽게 읽기 위한 유틸함수가 있습니다. <br>
다음과 같이 import 하여 사용합니다.

```python 
from marcap import marcap_data
```

### marcap_data(date)
지정한 날짜의 시가총액 순위 데이터를 읽어 옵니다

### marcap_data(start, end, code=None)
지정한 기간 데이터 읽어옵니다. 종목코드(code)를 지정하면 해당 종목에 대한 데이터를 지정한 기간만큼 읽어 옵니다.

간단한 사용 예제를 살펴보면,


```python
# 특정 날짜를 지정하여 읽기
df = marcap_data('2021-01-21')

# 기간을 지정하여 읽기 (2018년 1년간 전종목)
df = marcap_data('2020-01-01', '2020-12-31')

# 기간을 지정하여, 특정 종목 읽기 (2018년 1년간 특정 종목)
df = marcap_data('2021-01-01', '2021-01-31', code='005930')

# 1995-05-02 ~ 2021-01-15일까지 25년 데이터를 모두
df = marcap_data('1995-05-02', '2021-01-15')
```

## 시가총액 데이터셋(marcap) 튜토리얼

보다 상세한 내용은 주피터 노트북으로 튜토리얼 문서를 참고하십시오. (구글 Colab에서도 실행해 볼 수 있습니다)

1. [marcap-tutorial-01-reading-data.ipynb - 데이터 읽기](http://nbviewer.jupyter.org/fdd6518fa764911684b341f99bb61382)
1. [marcap-tutorial-02-stocks.ipynb - 종목별 분석](http://nbviewer.jupyter.org/51e998c745d8a05996f8967823dbf634)
1. [marcap-tutorial-03-adjust-price.ipynb - 수정가격](http://nbviewer.jupyter.org/b92cc4b901e7988956104b5f6483ee2e)
1. [marcap-tutorial-04-sector-analysis.ipynb - 섹터분석](http://nbviewer.jupyter.org/157e4083f482c8cf2c30e68ce7f7b942)


**2018-2021 [FinanceData.KR]()**
