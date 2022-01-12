from typing import Protocol, Union

from tweepy import Client, User
from tweepy.errors import BadRequest


class FollowEachOtherProvider(Protocol):
    @property
    def unexpected_error(self) -> bool:
        ...

    @property
    def account_exits(self) -> bool:
        ...

    def is_following(self) -> bool:
        ...


class BasicFollowEachOtherProvider:
    def __init__(self, client: Client, dev_username: str, dev_to_follow: str):
        self.client = client
        self.dev_username = dev_username
        self.dev_to_follow = dev_to_follow
        self.user_id: Union[int, None] = None
        self.bad_request_messages = []
        # the only-known error is the user not found
        self._unexpected_error = False

        self.look_for_id()

    @property
    def unexpected_error(self) -> bool:
        return self._unexpected_error

    def get_bad_request_messages(self) -> list[str]:
        return self.bad_request_messages

    @property
    def account_exits(self) -> bool:
        return bool(self.user_id)

    def look_for_id(self):
        try:
            res = self.client.get_user(username=self.dev_username, user_fields=["id"])
            if res.data:
                user: User = res.data
                self.user_id = user.id
        except BadRequest as bd:
            # should log errros
            self.bad_request_messages.extend(bd.api_messages)
        except Exception as e:
            # should log errros
            print(e)
            self._unexpected_error = True

    def is_following_from_data(self, users: Union[list[User], None]):
        if users:
            for u in users:
                if u.username == self.dev_to_follow:
                    return True
        return False

    def is_following(self) -> bool:
        if not self.user_id:
            return False

        try:
            res = self.client.get_users_following(id=self.user_id)
            isf = self.is_following_from_data(res.data)
            next_token = res.meta.get("next_token", None)
            # no 'do while' in python, to keep simple, we repeat the code
            while not isf and next_token:
                res = self.client.get_users_following(id=self.user_id)
                next_token = res.meta.get("next_token", None)
                isf = self.is_following_from_data(res.data)

            return isf
        except BadRequest as bd:
            # should log errros
            self._unexpected_error = True
            self.bad_request_messages.extend(bd.api_messages)
        except Exception as e:
            # should log errros
            print(e)
            self._unexpected_error = True

        return False
