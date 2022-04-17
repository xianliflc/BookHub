

import hashlib
from src.libs.objects.remote_item_object import RemoteItemObject


class RemoteRepo():

    def __init__(
        self,
        name: str,
        resource_vendor: str,
        url: str,
        resource_items: list[RemoteItemObject],
        version: int,
        maintainer: str,
        tags: list[str],
        description: str = "",
    ) -> None:
        self.name = name
        self.resource_vendor = resource_vendor
        self.url = url
        self.resource_items = resource_items
        self.version = version
        self.maintainer = maintainer
        self.tags = tags
        self.description = description
        self.id = None

    @property
    def is_initialized(self):
        if not self.id:
            return False

        for item in self.items:
            if not item.is_initialized:
                return False

        return True

    def initialize(self):
        the_string = ' '.join(
            [
                self.name,
                self.resource_vendor,
                self.url,
                str(self.version),
                self.maintainer
            ]
        )
        self.id = hashlib.md5(the_string.encode()).hexdigest()
        for k in range(len(self.resource_items)):
            self.resource_items[k].initialize()

    @staticmethod
    def get_build_params(data: dict):
        data['resource_vendor'] = data.get('resource_vendor', 'Github')

        return data



class RemoteRepos():
    def __init__(self, repos: list[RemoteRepo]) -> None:
        self.repos = repos
