from __future__ import annotations


class Client:
    def __init__(self) -> None:
        self.me = User("username")

    async def get_me(self):
        return self.me


class User:
    def __init__(self, username: str | None = None) -> None:
        self.username = username


class Message:
    def __init__(self, text: str | None = None, caption: str | None = None) -> None:
        self.text = text
        self.caption = caption
        self.command = None
