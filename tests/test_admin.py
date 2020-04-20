def test_admin_config(server):
    resp = server.admin_config()
    #TODO-36 check response as expected
    assert resp.status_code == 200
    return

def test_admin_status(server):
    resp = server.admin_status()
    #TODO-36 check response as expected
    assert resp.status_code == 200
    assert resp.json().get('id_len') == 0
    return