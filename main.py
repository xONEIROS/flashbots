
import time
import requests
from web3 import Web3
import schedule

infura_url = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'
web3 = Web3(Web3.HTTPProvider(infura_url))
address = 'YOUR_WALLET_ADDRESS'
private_key = 'YOUR_PRIVATE_KEY'

recipient_address = 'RECIPIENT_WALLET_ADDRESS'
etherscan_api_key = 'YOUR_ETHERSCAN_API_KEY'
ifttt_event_name = 'YOUR_EVENT_NAME'
ifttt_key = 'YOUR_IFTTT_KEY'
ifttt_url = f'https://maker.ifttt.com/trigger/{ifttt_event_name}/with/key/{ifttt_key}'

def send_ifttt_notification(value1, value2, value3):
    data = {'value1': value1, 'value2': value2, 'value3': value3}
    requests.post(ifttt_url, json=data)

def get_eth_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    data = response.json()
    return data['ethereum']['usd']

def get_token_contracts(wallet_address):
    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&address={wallet_address}&tag=latest&apikey={etherscan_api_key}"
    response = requests.get(url).json()
    tokens = {}
    for token in response.get('result', []):
        token_address = token['contractAddress']
        token_symbol = token['symbol']
        tokens[token_symbol] = token_address
    return tokens

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

schedule.every().hour.do(send_eth_and_tokens)

while True:
    schedule.run_pending()
    time.sleep(1)
