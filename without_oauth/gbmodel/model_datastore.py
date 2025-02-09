from google.cloud import datastore
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    def __init__(self):
        self.client = datastore.Client(project='cloud-varun-varunch',namespace="apiverse")


    def get_user(self, email):
        """Fetch a user by email."""
        query = self.client.query(kind='User')
        query.add_filter('email', '=', email)
        users = list(query.fetch())
        return users[0] if users else None

    def insert_user(self, name, email, password):
        """Insert user details into Datastore if not exists."""
        if self.get_user(email):
            return False  # User already exists

        if not email.endswith("@pdx.edu"):
            return False  # Restrict non-PDX users

        hashed_password = generate_password_hash(password)

        key = self.client.key('User')
        user = datastore.Entity(key)
        user.update({
            'name': name,
            'email': email,
            'password': hashed_password
        })
        self.client.put(user)
        return True

    def verify_user(self, email, password):
        """Verify user login credentials."""
        user = self.get_user(email)
    
        # If user exists, check if password key exists before verifying
        if user and "password" in user:
            if check_password_hash(user["password"], password):
                return user  # ✅ Successful authentication
    
        return None  

