# Wether_logger_LADPS
---

# 🌤️ 기상청 LDAPS 예보 자동 기록기 (Weather Logger)

기상청 국지예보모델(LDAPS) 데이터를 활용하여 **특정 목표 날짜(D-Day)** 의 날씨 예보가 시간 흐름에 따라 어떻게 변하는지 추적하고, **Google Sheets**에 자동으로 기록하는 파이썬 봇입니다.

중요한 일정(시험, 행사 등)을 앞두고 기상 변화 추이를 정밀하게 모니터링하기 위해 제작되었습니다.

## ✨ 주요 기능

* **정밀한 데이터 수집**: 기상청 API(LDAPS)를 통해 3시간 단위의 국지 예보 데이터를 수집합니다.
* **스마트 시간 감지**: 실행되는 시간에 맞춰 가장 최신의 발표 데이터(Base Time: 03, 09, 15, 21시)를 자동으로 선택합니다.
* **클라우드 저장**: `gspread` 라이브러리를 통해 로컬 파일이 아닌 Google Sheets에 데이터를 저장하여 모바일에서도 확인이 가능합니다.
* **보안**: 민감한 API 키와 인증 정보는 외부 설정 파일(`config.json`)로 분리하여 안전하게 관리합니다.

## 🛠️ 사전 준비 (Prerequisites)

이 프로젝트를 실행하기 위해서는 아래의 준비물이 필요합니다.

1. **Python 3.x** 설치
2. **기상청 공공데이터 포털 API Key** (LDAPS 조회 서비스)
3. **Google Cloud Platform 서비스 계정 Key** (`.json` 파일)
4. 기록할 **Google Spreadsheet** 생성

## 📦 설치 및 설정 (Installation)

### 1. 라이브러리 설치

필요한 파이썬 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt

```

### 2. 설정 파일 생성 (중요!)

`config_sample.json` 파일의 이름을 `config.json`으로 변경한 뒤, 본인의 정보를 입력하세요.

```json
{
  "api_key": "여기에_기상청_API_키를_입력하세요",
  "dong_code": "4617058000",
  "target_date": "20260211",
  "sheet_name": "날씨기록",
  "google_auth_file": "service_key.json"
}

```

* `dong_code`: 기상청 행정구역코드 (기본값: 나주 영산동)
* `target_date`: 예보를 추적하고 싶은 날짜 (YYYYMMDD)
* `google_auth_file`: 구글 서비스 계정 인증 파일명

## 💡 Tip: 행정구역코드(dong_code) 찾는 법
dong_code는 기상청에서 사용하는 고유한 지역 번호입니다.

**[공공데이터포털 기상청 API 페이지]**에 접속합니다.

참고문서/상세설명 란에 있는 '행정구역코드(엑셀 파일)' 를 다운로드합니다.

파일을 열어 Ctrl + F로 본인이 사는 동네(예: 영산동, 역삼동 등)를 검색합니다.

해당하는 10자리 코드를 복사하여 config.json에 붙여넣으세요.

### 3. 구글 시트 공유 설정

1. 구글 스프레드시트를 생성하고 이름을 `config.json`에 적은 `sheet_name`과 똑같이 맞춥니다.
2. 다운로드 받은 구글 인증 JSON 파일을 열어 `client_email` 주소를 복사합니다.
3. 스프레드시트 우측 상단 **[공유]** 버튼을 누르고 해당 이메일을 초대(편집자 권한)합니다.

## 🚀 사용 방법 (Usage)

### 수동 실행

터미널에서 아래 명령어를 입력하면 즉시 데이터를 수집하여 시트에 한 줄을 추가합니다.

```bash
python weather_gsheet.py

```

### 자동 실행 (Windows 작업 스케줄러)

매시간 자동으로 기록하려면 Windows 작업 스케줄러를 사용하는 것이 좋습니다.

1. `run.bat` 파일을 생성하여 아래 내용을 적습니다.
```batch
@echo off
python "C:\경로\weather-logger\weather_gsheet.py"

```


2. **작업 스케줄러**를 열고 '기본 작업 만들기'를 클릭합니다.
3. 트리거를 **'매일', '1시간 간격'** 으로 설정합니다.
4. 동작으로 위에서 만든 `run.bat` 파일을 지정합니다.

## 📂 파일 구조

```
weather-logger/
├── weather_gsheet.py    # 메인 실행 코드
├── config.json          # 사용자 설정 (Git 업로드 X)
├── config_sample.json   # 설정 예시 파일
├── requirements.txt     # 필요 라이브러리 목록
├── service_key.json     # 구글 인증 키 (Git 업로드 X)
└── README.md            # 프로젝트 설명서

```

## 📝 License

This project is licensed under the MIT License.

---
