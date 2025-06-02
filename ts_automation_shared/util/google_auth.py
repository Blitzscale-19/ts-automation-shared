from google.oauth2 import service_account
from google.auth.transport.requests import Request
from typing import Dict, List, Optional


class GoogleAuthService:
    def __init__(self, service_account_info: Dict, scopes: List[str]):
        """
        Initializes the GoogleAuthService with credentials and scopes.

        :param service_account_info: Dictionary with service account key data.
        :param scopes: List of OAuth scopes.
        """
        self.service_account_info = service_account_info
        self.scopes = scopes

    def get_access_token(self, subject: Optional[str] = None) -> str:
        """
        Returns an access token for the service account, optionally impersonating a user.

        :param subject: Optional user email to impersonate (domain-wide delegation).
        :return: Access token string.
        :raises: Exception if token generation fails.
        """
        try:
            credentials = service_account.Credentials.from_service_account_info(
                self.service_account_info,
                scopes=self.scopes,
                subject=subject
            )
            credentials.refresh(Request())
            return credentials.token
        except Exception as e:
            raise RuntimeError(f"Error generating access token: {e}") from e
