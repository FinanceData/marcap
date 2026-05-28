#-*- coding: utf-8 -*-
# krx_marcap.py
import os
import re
import glob
import csv
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
import requests

# Determine year_csv_dir dynamically based on directory structure
script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(script_dir, 'data')):
    year_csv_dir = os.path.join(script_dir, 'data')
elif os.path.exists(os.path.join(script_dir, 'marcap', 'data')):
    year_csv_dir = os.path.join(script_dir, 'marcap', 'data')
else:
    year_csv_dir = os.path.join(script_dir, 'data')

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0'

import time

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'referer': 'https://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

LOGIN_PAGE = "https://data.krx.co.kr/contents/MDC/COMS/client/MDCCOMS001.cmd"
LOGIN_JSP = "https://data.krx.co.kr/contents/MDC/COMS/client/view/login.jsp?site=mdc"
LOGIN_URL = "https://data.krx.co.kr/contents/MDC/COMS/client/MDCCOMS001D1.cmd"

_global_session = None
_session_expiry = 0

def load_env():
    """Load env variables from .env file if it exists."""
    # Check current script directory
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.exists(env_path):
        # Fallback to parent directory (e.g. if script is inside 'marcap' folder)
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")

def warmup_krx_session(session):
    session.get(LOGIN_PAGE, headers={"User-Agent": USER_AGENT}, timeout=15, verify=False)
    session.get(
        LOGIN_JSP,
        headers={"User-Agent": USER_AGENT, "Referer": LOGIN_PAGE},
        timeout=15,
        verify=False
    )

def login_krx(login_id, login_pw, session):
    warmup_krx_session(session)
    payload = {
        "mbrNm": "",
        "telNo": "",
        "di": "",
        "certType": "",
        "mbrId": login_id,
        "pw": login_pw,
    }
    headers_login = {"User-Agent": USER_AGENT, "Referer": LOGIN_PAGE}
    resp = session.post(LOGIN_URL, data=payload, headers=headers_login, timeout=15, verify=False)
    
    try:
        data = resp.json()
    except Exception as e:
        print(f"Failed to parse login response: {e}")
        return False
        
    error_code = data.get("_error_code", "")
    error_message = data.get("_error_message", "")

    if error_code == "CD010":
        print("⚠️ KRX 비밀번호 변경이 필요합니다.")
        print(f"   오류 메시지: {error_message}")
        print("   https://www.krx.co.kr 에서 비밀번호를 변경한 후 다시 시도하세요.")
        return False

    if error_code == "CD011":
        payload["skipDup"] = "Y"
        resp = session.post(LOGIN_URL, data=payload, headers=headers_login, timeout=15, verify=False)
        try:
            data = resp.json()
        except Exception:
            return False
        error_code = data.get("_error_code", "")

    return error_code == "CD001"

def get_session():
    global _global_session, _session_expiry
    load_env()
    login_id = os.getenv("KRX_ID")
    login_pw = os.getenv("KRX_PW")
    
    if not login_id or not login_pw:
        print("Error: KRX_ID or KRX_PW is not set. Please set them in your environment variables or a .env file.")
        return None
        
    if _global_session is not None and time.time() < _session_expiry:
        return _global_session
        
    print("KRX 로그인 시도 중...")
    session = requests.Session()
    session.headers.update(headers)
    
    if login_krx(login_id, login_pw, session):
        print("KRX 로그인 성공.")
        _global_session = session
        _session_expiry = time.time() + 3300  # 55 mins
        return _global_session
    else:
        print("KRX 로그인 실패. ID/PW를 확인해 주세요.")
        return None

def krx_marcap(date=None):
    '''
    전종목 시세 (정보데이터시스템 / 주식 / 종목 시세 / 전종목 시세)
    1995-05-02 ~ 현재까지    
    '''
    date = datetime.today() if date == None else pd.to_datetime(date)
    url = 'https://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
        'locale': 'ko_KR',
        'mktId': 'ALL',
        'trdDd': f'{date.strftime("%Y%m%d")}',
        'share': '1', # 1=주, 2=천주, 3=백만주
        'money': '1', # 1=원, 2=천원, 3=백만원, 4=십억원
        'csvxls_isNo': 'false',
    }
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    session = get_session()
    if session is None:
        return None
    r = session.post(url, data=data, verify=False)
    
    # 응답 상태 코드 확인
    if r.status_code != 200:
        print(f'Error: Received status code {r.status_code}')
        print(r.text)  # 응답 내용을 출력하여 확인
        return None

    try:
        j = json.loads(r.text)
    except json.JSONDecodeError as e:
        print(f'JSON decode error: {e}')
        print(r.text)  # 오류 발생 시 응답 내용을 출력
        return None

    if not j['OutBlock_1']:
        print('조회된 데이터가 없습니다')
        return None

    df = pd.json_normalize(j['OutBlock_1'])
    cols_map = {'ISU_SRT_CD':'Code', 'ISU_ABBRV':'Name', 
                'TDD_CLSPRC':'Close', 'SECT_TP_NM': 'Dept', 'FLUC_TP_CD':'ChangeCode', 
                'CMPPREVDD_PRC':'Changes', 'FLUC_RT':'ChangesRatio', 'ACC_TRDVOL':'Volume', 
                'ACC_TRDVAL':'Amount', 'TDD_OPNPRC':'Open', 'TDD_HGPRC':'High', 'TDD_LWPRC':'Low',
                'MKTCAP':'Marcap', 'LIST_SHRS':'Stocks', 'MKT_NM':'Market', 'MKT_ID': 'MarketId' }
    df = df[cols_map.keys()]
    df = df.rename(columns=cols_map)

    df['ChangesRatio'] = pd.to_numeric(df['ChangesRatio'].str.replace(',', ''), errors='coerce')
    int_cols = ['Close', 'Changes', 'Open', 'High', 'Low', 'Volume', 'Amount', 'Marcap', 'Stocks']
    for col in int_cols: 
        df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')

    df.sort_values('Marcap', ascending=False, inplace=True)
    df['Rank'] = np.arange(1, len(df) + 1)
    return df

if __name__ == "__main__":
    load_env()
    
    # Determine start_date and year range for data collection
    start_year_env = os.environ.get("START_YEAR")
    end_year_env = os.environ.get("END_YEAR")
    
    if start_year_env:
        start_date = f"{start_year_env}-01-01"
        start_year = int(start_year_env)
    elif os.environ.get("GITHUB_ACTIONS"):
        # Default to current year in GitHub Actions to run quickly
        current_year = datetime.today().year
        start_date = f"{current_year}-01-01"
        start_year = current_year
    else:
        # Default to full history in local runs
        start_date = "1995-05-02"
        start_year = 1995

    if end_year_env:
        end_year = int(end_year_env)
    else:
        end_year = datetime.today().year

    ## CSV 데이터 업데이트
    day_csv_dir = 'marcap_day_csv'
    for dt in pd.date_range(start_date, datetime.today() - timedelta(days=1)):
        year_dir = f"{day_csv_dir}/{dt.year}"
        os.makedirs(year_dir, exist_ok=True)
        fn = f"{year_dir}/marcap-{dt.strftime('%Y%m%d')}.csv"
        if os.path.exists(fn):
            continue
        print(dt)
        df = krx_marcap(dt)
        df.to_csv(fn, index=False, quoting=csv.QUOTE_ALL)
        print(fn)
    print('-' * 80)

    # 년도별로 묶어서 Parquet로 저장
    for year in range(start_year, end_year + 1):
        csv_list = sorted(glob.glob(f'{day_csv_dir}/{year}/marcap-{year}*.csv'))
        df_list = []
        for p in csv_list:
            df = pd.read_csv(p)
            df['Date'] = pd.to_datetime(re.findall(r'marcap-(\d+)\.csv', p)[0])
            df_list.append(df)

        if len(df_list) == 0:
            continue
        df_marcap = pd.concat(df_list, sort=False)
        df_marcap = df_marcap.dropna(subset=['Volume'])
        
        # 문자열 컬럼을 명시적으로 문자열로 변환 (parquet 저장 시 타입 오류 방지)
        str_cols = ['Code', 'Name', 'Dept', 'ChangeCode', 'Market', 'MarketId']
        for col in str_cols:
            if col in df_marcap.columns:
                df_marcap[col] = df_marcap[col].astype(str)
        
        to = f'{year_csv_dir}/marcap-{year}.parquet'
        df_marcap.to_parquet(to, index=False, compression='snappy')
        print(to)
