import requests



def test_scan_status(server, data):
    server.reset()
    contact_id = data.valid_ids[0]
    prefix = contact_id[0:3]
    data = [{"id":contact_id}]
    server.send_status(contacts = data)
    resp = server.scan_status(contact_prefixes = [prefix])
    assert resp.json()['ids'] == data
    return



