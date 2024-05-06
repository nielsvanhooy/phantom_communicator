from functools import wraps

from phantom_communicator.command_blocks.command_block import CommandBlock


class command:
    def __init__(self, name=None, vendor=None, model=None, os=None):
        self.name = name
        self.vendor = vendor
        self.model = [model] if type(model) in [str, type(None)] else model
        self.os = os

    def register(self, model, method):
        model = model.upper() if model else None
        CommandBlock.register_command(self.name, self.vendor, model, self.os, method)

    def __call__(self, method):
        for model in self.model:
            self.register(model, method)
        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper