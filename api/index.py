# Vercel entrypoint. The real Flask app lives in app.py at the project root;
# importing it here lets Vercel's Python runtime pick up `app` as the handler.
# (Vercel serves everything under /public directly from its CDN, so this
#  function only ever renders the dynamic "/" page.)
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402,F401
