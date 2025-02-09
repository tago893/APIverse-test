import secrets

def generate_api_key():
    return secrets.token_urlsafe(32)  # 32-byte secure random key
key = generate_api_key()
print(key)