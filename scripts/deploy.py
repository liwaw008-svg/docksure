import json,re
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet

ROOT=Path(__file__).parents[1];ENV=(ROOT.parents[3]/'accounts.env').read_text()
key=re.search(r'^ACCOUNT_4_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',ENV,re.M).group(1).strip()

def find(value):
    if isinstance(value,dict):
        for name in ('contract_address','contractAddress'):
            if value.get(name):return value[name]
        if value.get('recipient') and str(value.get('tx_execution_result',''))=='1':return value['recipient']
        for child in value.values():
            result=find(child)
            if result:return result
    if isinstance(value,list):
        for child in value:
            result=find(child)
            if result:return result

account=create_account(account_private_key=key);client=create_client(chain=studionet,account=account)
tx=client.deploy_contract(code=(ROOT/'contracts/contract.py').read_text(),args=[]);print('deployTx',tx,flush=True)
receipt=client.wait_for_transaction_receipt(transaction_hash=tx,status='ACCEPTED',retries=80,interval=20000)
address=find(receipt)
if not address:raise RuntimeError(receipt)
print(json.dumps({'contract':address,'transaction':tx,'network':'StudioNet'}),flush=True)
