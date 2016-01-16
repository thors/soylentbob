

class User:
    def __init__(self, name):
        self.activity = 0
        self.commented_on_activity = 0

class Users:
    def __init__(self):
        self.users = {}
        
    def add(self, user):
        if not user in self.users.keys():
            self.users[user] = User()
            
    def delete(self, user):
        del self.users[user]

    def activity(self, user):
        if user in self.users.keys():
            self.users[user].activity = self.users[user].activity + 1
        else:
            self.add(user)
            
    def tick(self):
        for k in self.users.keys():
            if self.users[k].activity > 0:
                self.users[k].activity = self.users[k].activity -1
