class FakeCfgConn:
    def __init__(self):
        self.result = None

    async def prepare(self):
        return None

    async def get_version(self):
        self.result = "i am a fake version"
        return self

    async def get_config(self, **kwargs):
        self.result = "fake config"
        return self
