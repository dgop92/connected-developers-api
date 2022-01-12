from typing import Any, Protocol

import requests


class GitHubOrganizationProvider(Protocol):
    @property
    def unexpected_error(self) -> bool:
        ...

    @property
    def account_exits(self) -> bool:
        ...

    def get_organizations(self) -> list[dict[str, Any]]:
        ...


class BasicOrganizationProvider:
    def __init__(self, url: str):
        self.url = url
        self._account_exits = False
        self._unexpected_error = False

        self.make_request()

    def make_request(self):
        self.request = requests.get(self.url)
        if self.request.status_code == 404:
            self._account_exits = False
            return

        if self.request.status_code != 200:
            self._unexpected_error = True
            return

        self._account_exits = True

    @property
    def account_exits(self) -> bool:
        return self._account_exits

    @property
    def unexpected_error(self) -> bool:
        return self._unexpected_error

    def get_organizations(self) -> list[dict[str, Any]]:
        return self.request.json()
