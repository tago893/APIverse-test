import secrets
import hashlib
import time
from google.cloud import datastore
from datetime import datetime, timedelta, timezone
from flask import session

# Initialize Datastore Client with explicit namespace configuration
client = datastore.Client(project='cloud-varun-varunch', namespace="apiverse")

def generate_salt():
    """Generate a unique salt value."""
    return secrets.token_hex(16)  # 32-character salt (16 bytes)

def generate_api_key():
    """Generate a secure 64-byte random API key."""
    return secrets.token_urlsafe(64)  # 64-byte key

def hash_api_key(api_key, salt):
    """Hash the API key with a unique salt using SHA-256."""
    combined = f"{api_key}{salt}"  # Append salt to key
    return hashlib.sha256(combined.encode()).hexdigest()

def store_api_key(user_email, session):
    """Generate and store a unique API key using a salted hash."""
    client = datastore.Client(project='cloud-varun-varunch', namespace="apiverse")
    print(f"Datastore Client Namespace: {client.namespace}")

    raw_api_key = generate_api_key()  # Generate API key
    salt = generate_salt()  # Generate salt
    hashed_api_key = hash_api_key(raw_api_key, salt)  # Hash API key
    expiration_date = datetime.now(timezone.utc) + timedelta(days=30)  # Set expiration

    # Create key
    key = client.key('APIKey')
    print(f"Generated Key: {key}")

    # Create entity
    entity = datastore.Entity(key)
    entity.update({
        'user_email': user_email,
        'salt': salt,
        'hashed_api_key': hashed_api_key,
        'created_at': datetime.now(timezone.utc),
        'expires_at': expiration_date,
        'revoked': False
    })
    print(f"Entity Data to Save: {entity}")

    # Save entity to Datastore
    try:
        client.put(entity)
        print(f"API Key successfully saved for user: {user_email}")
    except Exception as e:
        print(f"Error saving API Key: {e}")

    # Store raw API key in session
    session['temp_api_key'] = {
        "api_key": raw_api_key,
        "expires_at": time.time() + 60  # Expiry timestamp
    }

    return raw_api_key

def get_user_api_keys(user_email):
    """Retrieve all non-revoked API keys for a given user, showing only masked versions."""
    query = client.query(kind='APIKey')
    query.add_filter('user_email', '=', user_email)
    query.add_filter('revoked', '=', False)  # Only return active keys
    api_keys = list(query.fetch())

    return [{
        'api_key_id': key.id,
        'masked_key': '************' + key['hashed_api_key'][-4:],  # Show only last 4 characters
        'expires_at': key['expires_at']  # Expiration date
    } for key in api_keys if datetime.now(timezone.utc) < key['expires_at']]

def validate_api_key(api_key):
    """Validate an API key by checking if it's valid, not expired, and not revoked."""
    query = client.query(kind='APIKey')
    results = list(query.fetch())

    for entry in results:
        salt = entry['salt']
        stored_hashed_key = entry['hashed_api_key']
        expires_at = entry['expires_at']
        revoked = entry.get('revoked', False)  # Check if key is revoked

        # Check if the key is expired
        if datetime.now(timezone.utc) > expires_at:
            return False  # Key is expired

        # Check if the key is revoked
        if revoked:
            return False  # Key has been revoked

        # Recompute the hash with the retrieved salt
        if stored_hashed_key == hash_api_key(api_key, salt):
            return True  # API key is valid

    return False  # No valid key found

def revoke_api_key(user_email, api_key_id):
    """Manually revoke an API key using its ID."""
    try:
        # Create key (namespace is already set in the client)
        key = client.key('APIKey', int(api_key_id))
        entity = client.get(key)

        if entity:
            if entity.get('user_email') == user_email:
                entity['revoked'] = True  # Mark as revoked
                client.put(entity)  # Save updated entity
                print(f"✅ API Key {api_key_id} revoked successfully.")
                return True
            else:
                print(f"❌ API Key {api_key_id} does not belong to {user_email}.")
        else:
            print(f"❌ API Key {api_key_id} not found in Datastore.")

    except Exception as e:
        print(f"❌ Error revoking API Key: {e}")

    return False  # Revocation failed
