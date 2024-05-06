from phantom_communicator.exceptions import SNMPCommandOIDMissingError


class SNMPCommand:
    agent = None
    oid = None
    community_string = None
    version = None

    def __init__(self, oid=None, agent=None, community_string=None, version=None):
        if not oid:
            raise SNMPCommandOIDMissingError("oid is required for initializing an SNMPCommand")

        self.agent = agent
        self.oid = oid
        self.community_string = community_string
        self.version = version