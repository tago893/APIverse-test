from flask import render_template, session, redirect, url_for, request
from flask.views import MethodView
from utils.api_key_generation import get_user_api_keys, store_api_key, revoke_api_key
import time

class Dashboard(MethodView):
    def get(self):
        """Display user details and API key management."""
        if 'user' not in session:
            print("User not in session! Redirecting to index...")
            return redirect(url_for('index'))  # Redirect to home if not logged in

        user_info = session['user']
        email = user_info['email']
        api_keys = get_user_api_keys(email)  # Fetch stored API keys

        # Check if there is a temporary API key in session
        temp_api_key = session.get('temp_api_key', None)
        if temp_api_key and time.time() < temp_api_key["expires_at"]:
            raw_api_key = temp_api_key["api_key"]
        else:
            raw_api_key = None  # Expired

        return render_template('dashboard.html',
                               name=user_info['name'],
                               email=email,
                               profile=user_info['picture'],
                               api_keys=api_keys,
                               raw_api_key=raw_api_key)

    def post(self):
        """Handle API key generation or revocation."""
        if 'user' not in session:
            return redirect(url_for('index'))

        email = session['user']['email']

        # ✅ Handle API key revocation
        revoke_key = request.form.get('revoke_key')
        if revoke_key:
            success = revoke_api_key(email, revoke_key)
            if success:
                print(f"✅ Successfully revoked API Key ID: {revoke_key}")
            else:
                print(f" Failed to revoke API Key ID: {revoke_key}")
            return redirect(url_for('dashboard'))  # Refresh dashboard after revocation

        # ✅ Generate a new API key
        raw_api_key = store_api_key(email, session)

        return redirect(url_for('dashboard'))  # Refresh dashboard after key creation


class GenerateKey(MethodView):
    def post(self):
        """Generate a new API key and redirect to dashboard."""
        print(" Generate API Key Button Clicked!")  # Debugging print

        if 'user' not in session:
            print(" User not in session! Redirecting to index...")
            return redirect(url_for('index'))

        email = session['user']['email']
        print(f"🔹 User Email Found: {email}")  # Debugging print

        raw_api_key = store_api_key(email, session)  # Store API key
        print(f"API Key Generated: {raw_api_key}")  # Debugging print

        return redirect(url_for('dashboard'))  # Refresh dashboard


