
import hashlib

class RemoteItemObject():
    def __init__(
        self,
        resource_item_name: str,
        author: str,
        resource_type: str,
        relative_url: str,
        description: str = "",
        id: str = None
    ) -> None:
        self.resource_item_name = resource_item_name
        self.author = author
        self.resource_type = resource_type
        self.relative_url = relative_url
        self.description = description
        self.id = id

    @property
    def is_initialized(self) -> bool:
        return False if not self.id else True

    def initialize(self):
        the_string = ' '.join(
            [
                self.resource_item_name,
                self.author,
                self.resource_type,
                self.relative_url,
                self.description
            ]
        )
        self.id = hashlib.md5(the_string.encode()).hexdigest()

    