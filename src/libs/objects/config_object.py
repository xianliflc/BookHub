

class ConfigObject():

    def __init__(
        self, 
        user: dict,
        system: dict
    ) -> None:
        self.user = user
        self.system = system

    @property
    def download_path(self):
        return self.system['download_path']

