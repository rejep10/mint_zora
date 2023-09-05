from web3 import Web3, HTTPProvider
from eth_account import Account
import requests
import time
from mint_abi import MINT_ABI
# Замените URL на URL вашего узла
node_url = "https://rpc.zora.energy"
proxy_url = "" # Введите ваш прокси в формате login:password@ip:port

number_of_nft = 1 #кол-во нфт которое хотите заминтить

# Чтение приватных ключей из файла
private_keys = []
with open("ayodude.txt", "r") as file:
    private_keys = file.read().splitlines()

# Создание объекта сессии для использования прокси
session = requests.Session()
session.proxies = {"http": proxy_url, "https": proxy_url}

# Создание объекта Web3 с использованием сессии
w3 = Web3(HTTPProvider(node_url, session=session))

# Адрес смарт-контракта и ABI (интерфейс контракта)
contract_address = "0x09dD68c87020055a19733a6CcD7bfc7e7DfB3483"
contract_abi =  MINT_ABI # Замените на реальный ABI



# Цикл по всем приватным ключам
for private_key in private_keys:
    # Создание объекта смарт-контракта
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    # Получение адреса кошелька из приватного ключа
    account = Account.from_key(private_key)
    wallet_address = account.address
    function_call = contract.functions.mintWithRewards(account.address, number_of_nft, "", "0x0000000000000000000000000000000000000000")
    function_cost = w3.to_wei("0.000777", "ether")
    value = function_cost * number_of_nft
    # Вызов функции "минт"
    transaction = function_call.build_transaction({
        "value": value,
        "gas": 2000000,
        "gasPrice": w3.to_wei("0.005", "gwei"),
        "nonce": w3.eth.get_transaction_count(wallet_address),
    })

    # Подпись и отправка транзакции
    signed_transaction = Account.sign_transaction(transaction, private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    explorer_domain = "https://explorer.zora.energy/"
    explorer_url = f"{explorer_domain}/tx/{transaction_hash.hex()}"
    print(f"Mint transaction hash for {wallet_address}: {explorer_url}")

    # Добавление задержки в секундах
    time.sleep(5)  # Замените на нужное количество секунд
