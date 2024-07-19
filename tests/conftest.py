import pytest

from phantom_communicator.communicators.base import Communicator
from tests.fake_cfg_conn import FakeCfgConn


@pytest.fixture(name="iosxe_communicator")
def fx_iosxe_communicator():
    """Unstructured cpe representations."""
    communicator = Communicator.factory(host="10.1.1.156", username="test008", password="lagen008", os="iosxe")
    communicator._cfg_conn = FakeCfgConn()
    return communicator


@pytest.fixture(name="vrp_communicator")
def fx_vrp_communicator():
    """Unstructured cpe representations."""
    communicator = Communicator.factory(host="10.1.1.131", username="test008", password="lagen008", os="vrp")
    communicator._cfg_conn = FakeCfgConn()
    return communicator


pytest_plugins = [
    "tests.fixtures.cisco_iosxe",
    "tests.fixtures.huawei_hvrp",
]
