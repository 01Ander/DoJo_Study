class UserProfile:
    def __init__(self, username: str):
        self.username = username
        self.followers = 0

    def add_follower(self):
        self.followers += 1
