import pytest

from phantom_communicator.communicators.base import Communicator
from phantom_communicator.exceptions import CommunicatorNotFound


async def test_unknown_vendor():
    with pytest.raises(CommunicatorNotFound):
        Communicator.factory(host="10.1.1.156", os="junos")
