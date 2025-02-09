from flask import render_template, session, redirect, url_for, request
from flask.views import MethodView
from utils.api_key_generation import get_user_api_keys, store_api_key, revoke_api_key
import time

class Dashboard(MethodView):
    def get(self):
        """Display user details and API key management."""
        if 'user' not in session:
            return redirect(url_for('index'))  # Redirect to home if not logged in

        user_info = session['user']
        email = user_info['email']
        api_keys = get_user_api_keys(email)  # Fetch stored API keys

        # Check if there is a temporary API key in session
        temp_api_key = session.get('temp_api_key', None)
        raw_api_key = None
        remaining_time = 0

        if temp_api_key:
            current_time = time.time()
            if current_time < temp_api_key["expires_at"]:
                # Make the key available temporarily
                raw_api_key = temp_api_key["api_key"]
                remaining_time = int(temp_api_key["expires_at"] - current_time)

        # Remove the temporary API key from the session immediately after rendering
        if 'temp_api_key' in session:
            del session['temp_api_key']  # Ensure key is invalidated after initial load

        return render_template(
            'dashboard.html',
            name=user_info['name'],
            email=email,
            api_keys=api_keys,
            raw_api_key=raw_api_key,
            remaining_time=remaining_time  # Pass remaining time to the template
        )

    def post(self):
        """Handle API key generation or revocation."""
        if 'user' not in session:
            return redirect(url_for('index'))

        email = session['user']['email']

        # Handle API key revocation
        revoke_key = request.form.get('revoke_key')
        if revoke_key:
            revoke_api_key(email, revoke_key)
            return redirect(url_for('dashboard'))  # Refresh dashboard after revocation

        # Generate a new API key
        store_api_key(email, session)

        return redirect(url_for('dashboard'))  # Refresh dashboard after key creation


class GenerateKey(MethodView):
    def post(self):
        """Generate a new API key and redirect to dashboard."""
        if 'user' not in session:
            return redirect(url_for('index'))

        email = session['user']['email']

        store_api_key(email, session)  # Store API key

        return redirect(url_for('dashboard'))  # Refresh dashboard
