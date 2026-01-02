import os
import time
import hashlib
import hmac
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# API 키 로드
API_KEY = os.environ.get("NAVER_AD_CLIENT_ID")
SECRET_KEY = os.environ.get("NAVER_AD_CLIENT_SECRET")
CUSTOMER_ID = os.environ.get("NAVER_AD_CUSTOMER_ID")

print(f"API_KEY: {API_KEY[:20]}..." if API_KEY else "API_KEY: None")
print(f"SECRET_KEY: {SECRET_KEY[:20]}..." if SECRET_KEY else "SECRET_KEY: None")
print(f"CUSTOMER_ID: {CUSTOMER_ID}")

# 헤더 생성
BASE_URL = "https://api.naver.com"
uri = "/keywordstool"
method = "GET"
timestamp = str(round(time.time() * 1000))

sign = f"{timestamp}.{method}.{uri}"
signature = hmac.new(
    SECRET_KEY.encode(),
    sign.encode(),
    hashlib.sha256
).digest()
signature_base64 = base64.b64encode(signature).decode()

headers = {
    "X-API-KEY": API_KEY,
    "X-Customer": CUSTOMER_ID,
    "X-Timestamp": timestamp,
    "X-Signature": signature_base64,
}

# 단일 키워드로 테스트
params = {
    "hintKeywords": "삼성전자",
    "showDetail": "1"
}

print(f"\n요청 URL: {BASE_URL + uri}")
print(f"Params: {params}")

response = requests.get(BASE_URL + uri, headers=headers, params=params)

print(f"\n상태 코드: {response.status_code}")
print(f"응답: {response.text[:500] if response.text else '(empty)'}")
