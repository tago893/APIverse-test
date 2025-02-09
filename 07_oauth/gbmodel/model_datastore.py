from datetime import datetime
from google.cloud import datastore

class UserModel:
    def __init__(self):
        self.client = datastore.Client('cloud-varun-varunch')

    def get_user(self, email):
        """Fetch a user by email."""
        query = self.client.query(kind='User')
        query.add_filter('email', '=', email)
        users = list(query.fetch())
        return users[0] if users else None

    def insert_user(self, name, email, profile):
        """Insert user details into Datastore if not exists."""
        if self.get_user(email):
            return False  # User already exists

        key = self.client.key('User')
        user = datastore.Entity(key)
        user.update({
            'name': name,
            'email': email,
            'profile': profile,
            'date': datetime.today()
        })
        self.client.put(user)
        return True
