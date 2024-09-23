# auth/oauth.py


import os
from authlib.integrations.starlette_client import OAuth


# Load environment variables for security
from dotenv import load_dotenv

load_dotenv()

# Configure Google OAuth
oauth = OAuth()

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    # access_token_url="https://accounts.google.com/o/oauth2/token",
    # authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid email profile"},
)
