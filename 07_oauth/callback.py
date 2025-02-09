from flask import redirect, request, url_for, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
from oauth_config import client_id, client_secret, token_url, redirect_callback
from gbmodel.model_datastore import UserModel  # Store user in database

class Callback(MethodView):
    def get(self):
        """Handles OAuth callback and stores user session."""
        google = OAuth2Session(client_id, redirect_uri=redirect_callback, state=session.get('oauth_state'))

        # ✅ Ensure HTTPS is used
        request_url = request.url.replace("http:", "https:")

        # Fetch OAuth token from Google
        token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=request_url)
        session['oauth_token'] = token  # ✅ Save token in session

        # Get user info from Google
        user_info = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
        session['user'] = user_info  # ✅ Store user info in session

        # Save user in Datastore if not already present
        user_model = UserModel()
        user_model.insert_user(user_info['name'], user_info['email'], user_info['picture'])

        return redirect(url_for('dashboard'))  # ✅ Redirect to dashboard after login
