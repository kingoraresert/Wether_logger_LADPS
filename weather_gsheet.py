import requests
import datetime
import gspread
import json  # 설정 파일 읽기용 라이브러리 추가
import os
from oauth2client.service_account import ServiceAccountCredentials
from xml.etree import ElementTree

# ==========================================
# [설정 파일 로더]
# 코드가 실행될 때 config.json 파일을 찾아서 읽어옵니다.
# ==========================================
def load_config():
    config_file = 'config.json'
    if not os.path.exists(config_file):
        print(f"❌ 오류: '{config_file}' 파일이 없습니다.")
        print("같은 폴더에 설정 파일을 만들어주세요.")
        return None
        
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_google_sheet():
    # 1. 설정 불러오기
    config = load_config()
    if not config: return

    # config.json에서 값 꺼내기
    MY_API_KEY = config.get('api_key')
    MY_DONG_CODE = config.get('dong_code')
    TARGET_DATE = config.get('target_date')
    SHEET_NAME = config.get('sheet_name')
    JSON_FILE = config.get('google_auth_file')

    # 필수 정보가 비어있는지 체크
    if "여기에" in MY_API_KEY or "본인의" in JSON_FILE:
        print("⚠️ 경고: config.json 파일에 본인의 API 키와 파일명을 입력해주세요!")
        return

    # --- 2. 구글 시트 연결 ---
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
        client = gspread.authorize(creds)
        
        sh = client.open(SHEET_NAME)
        worksheet = sh.sheet1
    except Exception as e:
        print(f"❌ 구글 시트 접속 실패: {e}")
        print(f"Tip: '{JSON_FILE}' 파일이 폴더에 있는지, 시트 이름 '{SHEET_NAME}'이 맞는지 확인하세요.")
        return

    # --- 3. 헤더 만들기 ---
    if not worksheet.get_all_values():
        header = ["수집일시", "예보대상일", "시간", "기온(℃)", "습도(%)", "풍속(m/s)", "강수(mm)", "발표기준시각"]
        worksheet.append_row(header)
        print("✅ 헤더 생성 완료")

    # --- 4. 기상청 데이터 수집 (스마트 로직 유지) ---
    url = "https://apihub.kma.go.kr/api/typ02/openApi/NwpModelInfoService/getLdapsUnisArea"
    now = datetime.datetime.now()
    log_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    current_hour = now.hour
    if 0 <= current_hour < 7:
        yesterday = now - datetime.timedelta(days=1)
        base_date = yesterday.strftime("%Y%m%d")
        base_time = f"{base_date}2100"
    elif 7 <= current_hour < 13:
        base_date = now.strftime("%Y%m%d")
        base_time = f"{base_date}0300"
    elif 13 <= current_hour < 19:
        base_date = now.strftime("%Y%m%d")
        base_time = f"{base_date}0900"
    else:
        base_date = now.strftime("%Y%m%d")
        base_time = f"{base_date}1500"

    print(f"--- 데이터 수집 중... ({log_time_str}) ---")
    print(f"ℹ️ 적용된 발표 기준 시각(BaseTime): {base_time}")

    target_hours = ["09", "12", "15", "18"]
    data_types = {"Temp": "기온", "Wspd": "풍속", "Rain": "강수", "Humi": "습도"}
    forecast_data = {h: {} for h in target_hours}

    for dtype, dname in data_types.items():
        params = {
            "authKey": MY_API_KEY, "dongCode": MY_DONG_CODE, "baseTime": base_time,
            "dataType": "XML", "numOfRows": "60", "pageNo": "1", "dataTypeCd": dtype
        }
        try:
            res = requests.get(url, params=params)
            if res.status_code == 200:
                root = ElementTree.fromstring(res.content)
                for item in root.findall(".//item"):
                    ft = item.findtext("fcstTime")
                    if not ft: continue
                    if ft[0:8] == TARGET_DATE and ft[8:10] in target_hours:
                        forecast_data[ft[8:10]][dname] = item.findtext("value")
        except Exception as e:
            print(f"API 에러 ({dname}): {e}")

    # --- 5. 구글 시트 저장 ---
    added_count = 0
    for hour in target_hours:
        if forecast_data[hour]:
            row = [
                log_time_str, TARGET_DATE, f"{hour}시",
                forecast_data[hour].get("기온", ""),
                forecast_data[hour].get("습도", ""),
                forecast_data[hour].get("풍속", ""),
                forecast_data[hour].get("강수", ""),
                base_time
            ]
            worksheet.append_row(row)
            added_count += 1
            print(f" -> {hour}시 데이터 기록 완료")

    if added_count > 0:
        print(f"✅ 총 {added_count}개의 데이터 저장 완료")
    else:
        print(f"⚠️ {TARGET_DATE} 데이터를 찾지 못했습니다.")

if __name__ == "__main__":
    update_google_sheet()