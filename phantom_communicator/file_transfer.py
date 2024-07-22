from scrapli_transfer_utils import AsyncSrapliTransferUtils


class FileTransferManager:
    def __init__(self, session):
        self.session = session

    async def file_transfer(  # pylint: disable=too-many-arguments
        self,
        operation,
        src,
        dst="",
        verify=True,
        device_fs=None,
        overwrite=False,
        force_config=False,
        cleanup=True,
    ):
        scp = AsyncSrapliTransferUtils(self.session)
        return await scp.file_transfer(
            operation=operation,
            src=src,
            dst=dst,
            verify=verify,
            device_fs=device_fs,
            force_config=force_config,
            cleanup=cleanup,
            overwrite=overwrite,
        )
