from conftest import CONTRACT

LANE='Casablanca terminal to Rotterdam cold-chain dock'
PROMISE='Delivery must be confirmed by the destination record before the booked deadline; only a documented authority closure excuses delay.'
RULES=['https://carrier.example/records/shipment-1','https://dock.example/receipts/shipment-1']

def opened(direct_vm,direct_deploy,direct_alice,direct_bob,key):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice;direct_vm.value=100
    c.open_shipment(key,'0x'+direct_bob.hex(),LANE,PROMISE,RULES);direct_vm.value=0;direct_vm.sender=direct_bob;c.accept_shipment(key)
    return c

def test_hostname_prefix_bypass_is_rejected(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=opened(direct_vm,direct_deploy,direct_alice,direct_bob,'HOST-BYPASS')
    with direct_vm.expect_revert('distinct customer-authorized source slot'):
        c.submit_delivery('HOST-BYPASS',['https://carrier.example.evil.test/records/shipment-1','https://dock.example/receipts/shipment-1'])

def test_two_records_cannot_reuse_one_authorized_slot(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=opened(direct_vm,direct_deploy,direct_alice,direct_bob,'SAME-SLOT')
    with direct_vm.expect_revert('distinct customer-authorized source slot'):
        c.submit_delivery('SAME-SLOT',['https://carrier.example/records/shipment-1','https://carrier.example/records/shipment-1/duplicate'])

def test_customer_can_recover_after_acceptance(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=opened(direct_vm,direct_deploy,direct_alice,direct_bob,'RECOVERY');direct_vm.sender=direct_alice
    c.recover_unsettled('RECOVERY')
    assert c.get_shipment('RECOVERY')['status']=='RECOVERED'
    with direct_vm.expect_revert('shipment not reviewable'):
        direct_vm.sender=direct_bob;c.submit_delivery('RECOVERY',RULES)
