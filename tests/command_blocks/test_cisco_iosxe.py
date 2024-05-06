

def test_basic(cb_cisco):
    assert cb_cisco.show_version().command == "show ver"
    assert cb_cisco.setup_session().command == "terminal length 0"