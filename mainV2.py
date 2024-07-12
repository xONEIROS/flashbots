import time
import aiohttp
import asyncio
from web3 import Web3
import schedule
import os

# اتصال به شبکه اتریوم
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

# آدرس کیف پول و کلید خصوصی (هرگز کلید خصوصی را به اشتراک نگذارید)
address = os.getenv('WALLET_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')

# آدرس دریافت‌کننده
recipient_address = os.getenv('RECIPIENT_WALLET_ADDRESS')

# کلید API از Etherscan
etherscan_api_key = os.getenv('ETHERSCAN_API_KEY')

# URL و Event Name برای Webhook IFTTT
ifttt_event_name = os.getenv('IFTTT_EVENT_NAME')
ifttt_key = os.getenv('IFTTT_KEY')
ifttt_url = f'https://maker.ifttt.com/trigger/{ifttt_event_name}/with/key/{ifttt_key}'

async def send_ifttt_notification(value1, value2, value3):
    async with aiohttp.ClientSession() as session:
        data = {'value1': value1, 'value2': value2, 'value3': value3}
        await session.post(ifttt_url, json=data)

async def get_eth_price():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd') as response:
            data = await response.json()
            return data['ethereum']['usd']

async def get_token_contracts(wallet_address):
    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&address={wallet_address}&tag=latest&apikey={etherscan_api_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            tokens = {}
            for token in data.get('result', []):
                token_address = token['contractAddress']
                token_symbol = token['symbol']
                tokens[token_symbol] = token_address
            return tokens

async def send_eth_and_tokens():
    eth_price = await get_eth_price()
    balance = web3.eth.get_balance(address)
    balance_in_usd = (balance / 10**18) * eth_price
    
    if balance_in_usd > 5:
        # ارسال اتریوم
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
        await send_ifttt_notification('ETH Sent', web3.toHex(tx_hash), f'Amount: {amount / 10**18} ETH')

        # ارسال توکن‌های ERC-20
        tokens = await get_token_contracts(address)
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
                await send_ifttt_notification(f'{token_name} Sent', web3.toHex(tx_hash), f'Amount: {token_balance / 10**18} {token_name}')
    else:
        print("Balance is less than $5. No transaction made.")

def schedule_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_eth_and_tokens())
    loop.close()

# زمان‌بندی اجرای اسکریپت هر ساعت یک‌بار
schedule.every().hour.do(schedule_task)

while True:
    schedule.run_pending()
    time.sleep(1)
