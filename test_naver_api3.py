import os
import time
import hashlib
import hmac
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("NAVER_AD_CLIENT_ID")
SECRET_KEY = os.environ.get("NAVER_AD_CLIENT_SECRET")
CUSTOMER_ID = os.environ.get("NAVER_AD_CUSTOMER_ID")

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

# 띄어쓰기 없는 키워드 테스트
params = {
    "hintKeywords": "종각역택시사고,전기차보조금",
    "showDetail": "1"
}

print(f"테스트 키워드: {params['hintKeywords']}")
response = requests.get(BASE_URL + uri, headers=headers, params=params)
print(f"상태 코드: {response.status_code}")
print(f"응답: {response.text[:500] if response.text else '(empty)'}")
