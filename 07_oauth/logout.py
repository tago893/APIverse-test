from flask import redirect, url_for, session
from flask.views import MethodView

class Logout(MethodView):
    def get(self):
        """Logs out the user by clearing the session and forcing Google OAuth logout."""
        print("✅ Logout requested!")
        session.clear()  # Clears session
        print(f"✅ Session after logout: {session}")  # Should be empty

        # Google Logout URL (forces logout from Google OAuth)
        google_logout_url = "https://accounts.google.com/Logout"

        return redirect(google_logout_url)  # Redirect to Google logout

