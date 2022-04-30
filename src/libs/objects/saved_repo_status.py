


from datetime import datetime
from src.libs.objects.local_file_object import LocalFileObject


class RepoStatus():
    def __init__(
        self,
        name: str,
        md5: str,
        created_from: str,
        updated_at: datetime,
        created_at: datetime,
        updates_detected_at: datetime = None,
        has_updates: bool = False,
        is_archieved: bool = False,
        downloaded_files: list[LocalFileObject] = []
    ) -> None:
        self.name = name
        self.md5 = md5
        self.created_from = created_from
        self.updated_at = updated_at
        self.created_at = created_at
        self.updates_detected_at = updates_detected_at
        self.has_updates = has_updates
        self.is_archieved = is_archieved
        self.downloaded_files = downloaded_files

class ReposStatus():
    def __init__(self, repos: list[RepoStatus]) -> None:
        self.repos = repos