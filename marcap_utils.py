# -*- coding: utf-8 -*-
# marcap_utils.py - 시가총액 데이터를 위한 유틸함수

from datetime import datetime
import numpy as np
import pandas as pd
import glob

def marcap_date(date):
  '''
  지정한 날짜의 시가총액 순위 데이터
  :param datetime theday: 날짜
  :return: DataFrame
  '''
  date = pd.to_datetime(date)
  csv_file = 'marcap/data/marcap-%s.csv.gz' % (date.year)
  result = None
  try: 
    dtypes={'Code':str, 'Name':str, 
            'Open':float, 'High':float, 'Low':float, 'Close':float, 'Volume':float, 'Amount':float,
            'Changes':float, 'ChagesRatio':float, 'Marcap':float, 'Stocks':float, 'MarcapRatio':float, 
            'ForeignShares':float, 'ForeignRatio':float, 'Rank':float}

    df = pd.read_csv(csv_file, dtype=dtypes, parse_dates=['Date'])
    cols = ['Date', 'Code', 'Name',
            'Open', 'High', 'Low', 'Close', 'Volume', 'Amount', 
            'Changes', 'ChagesRatio', 'Marcap', 'Stocks', 'MarcapRatio', 
            'ForeignShares', 'ForeignRatio', 'Rank']
    result = df[cols]
    result = result[result['Date'] == date]
    result = result.sort_values(['Date','Rank'])
  except Exception as e:
    print(e)
    return None
  result.set_index('Date', inplace=True)
  return result[result['Volume'] > 0]

def marcap_date_range(start, end=None, code=None):
  '''
  지정한 기간 데이터 가져오기
  :param datetime start: 시작일
  :param datetime end: 종료일
  :param str code: 종목코드 (지정하지 않으면 모든 종목)
  :return: DataFrame
  '''
  start = pd.to_datetime(start)
  end = start if end==None else pd.to_datetime(end)
  df_list = []

  dtypes={'Code':str, 'Name':str, 
          'Open':float, 'High':float, 'Low':float, 'Close':float, 'Volume':float, 'Amount':float,
          'Changes':float, 'ChagesRatio':float, 'Marcap':float, 'Stocks':float, 'MarcapRatio':float, 
          'ForeignShares':float, 'ForeignRatio':float, 'Rank':float}

  for year in range(start.year, end.year + 1):
    try:
      csv_file = 'marcap/data/marcap-%s.csv.gz' % (year)
      df = pd.read_csv(csv_file, dtype=dtypes, parse_dates=['Date'])
      df_list.append(df)
    except Exception as e:
      print(e)
      pass
  df_merged = pd.concat(df_list)
  df_merged = df_merged[(start <= df_merged['Date']) & (df_merged['Date'] <= end)]  
  df_merged = df_merged.sort_values(['Date','Rank'])
  if code:
    df_merged = df_merged[code == df_merged['Code']]  
  df_merged.set_index('Date', inplace=True)
  return df_merged[df_merged['Volume'] > 0]

