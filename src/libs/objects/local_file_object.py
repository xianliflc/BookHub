

import datetime

class Tag():
    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id

class VirtualFolder(Tag):
    def __init__(self, name: str, id: int) -> None:
        super().__init__(name, id)

class LocalFileObject():
    def __init__(
        self,
        path: str,
        id: str,
        created_at: datetime = datetime.datetime.now(),
        updated_at: datetime = datetime.datetime.now(),
        opened_at: datetime = None
    ) -> None:
        self.path = path
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.opened_at = opened_at


    

