from phantom_communicator.exceptions import GenieCommandMissingError


class GenieCommand:
    genie_command = None

    def __init__(self, real_command, genie_command=None):
        self.real_command = real_command
        self.genie_command = genie_command
        if not genie_command:
            raise GenieCommandMissingError(
                "genie command is required for initialisation an GenieCommand"
            )