import requests
import json

text_to_explain = "Сумма квадратов a **2 + b**2 и отличия от ( a + b ) **2."

url = "http://127.0.0.1:8000/explain"

response = requests.post(url, data=text_to_explain.encode("utf-8"))
output_json = response.json()

print(json.dumps(output_json, indent=2, ensure_ascii=False))