def test_basic(cb_huawei):
    assert cb_huawei.show_startup_config().command == "display saved-configuration"
