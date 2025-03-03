import os
from google.cloud import secretmanager
import logging

logger = logging.getLogger(__name__)

# Secret Manager Client
secret_client = secretmanager.SecretManagerServiceClient()

# Function to fetch secrets from Secret Manager
def get_secret(secret_id):
    try:
        project_id = "ghost-name-app-452412"
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = secret_client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Failed to fetch secret {secret_id}: {str(e)}")
        raise

# Load secrets into environment variables
try:
    client_id = get_secret("oauth-client-id")
    client_secret = get_secret("oauth-client-secret")
    logger.info(f"Fetched CLIENT_ID: {client_id}")
    logger.info(f"Fetched CLIENT_SECRET: {client_secret[:4]}...")
    os.environ["OAUTH_CLIENT_ID"] = client_id
    os.environ["OAUTH_CLIENT_SECRET"] = client_secret
except Exception as e:
    logger.error(f"Startup failed due to secret loading: {str(e)}")
    raise

# Determine environment (local or production)
IS_LOCAL = os.environ.get("GAE_ENV", "standard") != "standard"
REDIRECT_URI = "http://127.0.0.1:8080/callback" if IS_LOCAL else "https://ghost-name-app-452412.appspot.com/callback"

# Google OAuth Config
CLIENT_SECRETS = {
    "web": {
        "client_id": os.environ["OAUTH_CLIENT_ID"],
        "client_secret": os.environ["OAUTH_CLIENT_SECRET"],
        "redirect_uris": [REDIRECT_URI],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token"
    }
}
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]