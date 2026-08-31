import json,re,time
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet

ROOT=Path(__file__).parents[1]; ENV=(ROOT.parents[3]/'accounts.env').read_text()
def secret(n):return re.search(rf'^ACCOUNT_{n}_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',ENV,re.M).group(1).strip()
def wait(c,h):
    r=c.wait_for_transaction_receipt(transaction_hash=h,status='ACCEPTED',retries=120,interval=10000)
    t=c.get_transaction(transaction_hash=h)
    if t.get('status_name')!='ACCEPTED' or t.get('result') not in (6,'6'):raise RuntimeError({'status':t.get('status_name'),'result':t.get('result')})
    return r

customer=create_account(account_private_key=secret(3)); carrier=create_account(account_private_key=secret(4))
cc=create_client(chain=studionet,account=customer); kc=create_client(chain=studionet,account=carrier)
address=json.loads((ROOT/'deployment.json').read_text())['contract']; shipment='DS-POLICY-'+str(int(time.time()))
base='https://raw.githubusercontent.com/liwaw008-svg/docksure/bff03a0'
sources=[base+'/evidence/demo-carrier-record.json',base+'/evidence/demo-dock-receipt.json']
promise='Destination receipt must confirm delivery before 2026-08-31T16:00:00Z with an intact seal. Only a documented public-authority closure or severe-weather event excuses delay.'
opened=cc.write_contract(address=address,function_name='open_shipment',args=[shipment,carrier.address,'Casablanca terminal to Rotterdam cold-chain dock',promise,sources],value=10**16);print('fund',opened,flush=True);wait(cc,opened)
accepted=kc.write_contract(address=address,function_name='accept_shipment',args=[shipment]);print('accept',accepted,flush=True);wait(kc,accepted)
try:
    kc.simulate_write_contract(address=address,function_name='submit_delivery',args=[shipment,['https://example.com/a','https://example.org/b']])
    raise RuntimeError('unauthorized evidence simulation unexpectedly passed')
except Exception as e:print('negative','unauthorized evidence rejected',flush=True)
settled=kc.write_contract(address=address,function_name='submit_delivery',args=[shipment,sources]);print('settle',settled,flush=True);wait(kc,settled)
state=kc.read_contract(address=address,function_name='get_shipment',args=[shipment]);print(json.dumps({'id':shipment,'customer':customer.address,'carrier':carrier.address,'transactions':{'fund':opened,'accept':accepted,'settle':settled},'state':state},indent=2),flush=True)
if state['status']!='SETTLED' or state['verdict'] not in ('ON_TIME','EXCUSED') or len(state['evidence_digests'])!=2:raise RuntimeError(state)
