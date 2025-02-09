class APIKeyModel:
    def __init__(self):
        """Initialize Datastore Client with 'apiverse' namespace."""
        self.client = datastore.Client(project='cloud-varun-varunch', namespace="apiverse")

    def store_api_key(self, user_email, session):
        """Generate and store a unique API key using a salted hash."""
        raw_api_key = self.generate_api_key()
        salt = self.generate_salt()
        hashed_api_key = self.hash_api_key(raw_api_key, salt)
        expiration_date = datetime.now(timezone.utc) + timedelta(days=30)

        # ✅ Ensure namespace is used when creating the key
        key = self.client.key('APIKey', namespace="apiverse")  # Namespace automatically applied by the client
        entity = datastore.Entity(key)
        entity.update({
            'user_email': user_email,
            'salt': salt,
            'hashed_api_key': hashed_api_key,
            'created_at': datetime.now(timezone.utc),
            'expires_at': expiration_date,
            'revoked': False
        })
        self.client.put(entity)

        print(f"✅ API Key stored in project: {self.client.project}, namespace: {self.client.namespace}")

        session['temp_api_key'] = {
            "api_key": raw_api_key,
            "expires_at": time.time() + 60
        }

        return raw_api_key

    def get_user_api_keys(self, user_email):
        """Retrieve all non-revoked API keys for a given user, showing only masked versions."""
        query = self.client.query(kind='APIKey', namespace="apiverse")
        query.add_filter('user_email', '=', user_email)
        query.add_filter('revoked', '=', False)
        api_keys = list(query.fetch())

        return [{
            'api_key_id': key.id,
            'masked_key': '************' + key['hashed_api_key'][-4:],  # Show only last 4 characters
            'expires_at': key['expires_at']
        } for key in api_keys if datetime.now(timezone.utc) < key['expires_at']]

    def revoke_api_key(self, user_email, api_key_id):
        """Manually revoke an API key using its ID."""
        try:
            key = self.client.key('APIKey', namespace="apiverse",int(api_key_id))  # ✅ Ensure namespace is used
            entity = self.client.get(key)

            if entity:
                if entity.get('user_email') == user_email:
                    entity['revoked'] = True
                    self.client.put(entity)
                    print(f"✅ API Key {api_key_id} revoked successfully.")
                    return True
                else:
                    print(f"❌ API Key {api_key_id} does not belong to {user_email}.")
            else:
                print(f"❌ API Key {api_key_id} not found in Datastore.")

        except Exception as e:
            print(f"❌ Error revoking API Key: {e}")

        return False
