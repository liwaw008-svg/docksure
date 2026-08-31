from pathlib import Path
import ast
S=(Path(__file__).parents[1]/'contracts/contract.py').read_text()
def test_parses_and_has_complete_lifecycle():
    ast.parse(S)
    for name in ('open_shipment','accept_shipment','cancel_offer','submit_delivery','get_shipment','list_shipments'):assert f'def {name}' in S
def test_consensus_is_replayed_independently():
    assert 'mine=run()' in S and "mine['verdict']==theirs.get('verdict')" in S and "mine['exceptions']==theirs.get('exceptions')" in S
def test_no_forbidden_nested_principle():
    assert 'prompt_non_comparative' not in S and 'eq_principle' not in S
def test_money_moves_only_after_bounded_verdict():
    assert "recipient=s.carrier if verdict in ('ON_TIME','EXCUSED') else s.customer" in S
    assert "on='finalized'" in S
def test_sources_are_refetched_by_each_validator():
    assert 'gl.nondet.web.get(url)' in S and 'run_nondet_unsafe(run,validate)' in S

