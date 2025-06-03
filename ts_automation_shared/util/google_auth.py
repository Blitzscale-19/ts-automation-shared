from google.oauth2 import service_account
from google.auth.transport.requests import Request
from typing import Dict, List, Optional

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/meetings.space.created",
    "https://www.googleapis.com/auth/meetings.space.readonly",
    "https://www.googleapis.com/auth/meetings.space.settings",
    "https://www.googleapis.com/auth/drive",
]

class GoogleAuthService:
    def __init__(self, service_account_info: Dict):
        """
        Initializes the GoogleAuthService with credentials and scopes.

        :param service_account_info: Dictionary with service account key data.
        :param scopes: List of OAuth scopes.
        """
        self.service_account_info = service_account_info

    def assign_scoped_and_get_access_token(self, subject: Optional[str] = None) -> str:
        """
        Returns an access token for the service account, optionally impersonating a user.

        :param subject: Optional user email to impersonate (domain-wide delegation).
        :return: Access token string.
        :raises: Exception if token generation fails.
        """
        try:
            credentials = service_account.Credentials.from_service_account_info(
                self.service_account_info,
                scopes=SCOPES,
                subject=subject
            )
            credentials.refresh(Request())
            return credentials.token
        except Exception as e:
            print(f"Error generating access token with delegation: {e}")
            return None

