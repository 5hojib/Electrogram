class Client:
    def __init__(self):
        self.me = User("username")

    async def get_me(self):
        return self.me


class User:
    def __init__(self, username: str = None):
        self.username = username


class Message:
    def __init__(self, text: str = None, caption: str = None):
        self.text = text
        self.caption = caption
        self.command = None
