from web3 import Web3
import subprocess, os, sys, json

# Use the Polygon network endpoint URL
polygon_rpc_url = "https://polygon-mainnet.infura.io/v3/9bc7411a1d4c4c1089fef2b26e7334a9"  # Replace with the correct Polygon network RPC URL

def scanContractInPeriod(web3, startBlockNumber, endBlockNumber):
    for i in range(startBlockNumber, endBlockNumber):
        print('Scanning block', i, '...')
        block = web3.eth.get_block(i)
        transactions = block['transactions']
        for transaction in transactions:
            receipt = web3.eth.get_transaction_receipt(transaction)
            if receipt['contractAddress']:
                contract = receipt['contractAddress'] + '\n'
                with open('ContractList.txt', 'a') as f:
                    f.write(contract)
    with open('ContractList.txt', 'a') as f:
        end = '... till block ' + str(endBlockNumber) + ' \n'
        f.write(end)

def auditContractByAddress(address):
    location = 'reports/' + address + '.md'
    if not os.path.isfile(location):
        with open(location, 'w') as f:
            subprocess.call(["myth", "-xia", address, "-o", "markdown", "--max-depth", "12", "-l"], stdout=f, stderr=f)
    else:
        print('Audit exists...')

def auditAllContractFound():
    with open('ContractList.txt', 'r') as f:
        for line in f:
            print('Auditing ' + line.rstrip('\n') + ' contract...\n')
            auditContractByAddress(line.rstrip('\n'))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Use argument -a to audit all contracts found, and -s to scan all contract till latest block!")
    elif sys.argv[1] == '-a':
        auditAllContractFound()
    elif sys.argv[1] == '-s':
        web3 = Web3(Web3.HTTPProvider(polygon_rpc_url))
        startBlockNumber = web3.eth.block_number - 100  # Replace the value with the number of blocks you want to go back for scanning
        endBlockNumber = web3.eth.block_number
        scanContractInPeriod(web3, startBlockNumber, endBlockNumber)
    else:
        print("Use argument -a to audit all contracts found, and -s to scan all contract till latest block!")
