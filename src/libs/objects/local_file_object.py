

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
        file_name: str,
        file_path: str,
        create_at: datetime = None,
        repo_id: str = None,
        remote_item_id: str = None,
        is_up_to_date: bool = True,
        has_update: bool = False,
        updated_at:datetime = datetime.datetime.now(),
        is_opened: bool = False,
        tags: list[Tag] = [],
        virtual_folder: VirtualFolder = None
    ) -> None:
        self.file_name = file_name
        self.file_path = file_path
        self.create_at = create_at
        self.is_up_to_date = is_up_to_date
        self.has_update = has_update
        self.updated_at = updated_at
        self.is_opened = is_opened
        self.has_update = has_update
        self.has_update = has_update
        self.repo_id = repo_id
        self.remote_item_id = remote_item_id
        self.tags = tags
        self.virtual_folder = virtual_folder

    @property
    def has_remote(self) -> bool:
        return self.repo_id is not None

    

