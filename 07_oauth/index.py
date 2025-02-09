from flask import render_template, session
from flask.views import MethodView

class Index(MethodView):
    def get(self):
        """Show home page and check if user is logged in."""
        user_info = session.get('user')  # Get user session data
        return render_template('index.html', is_logged_in=bool(user_info))
