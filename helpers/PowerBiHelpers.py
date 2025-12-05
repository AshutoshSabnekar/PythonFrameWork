"""
Power BI specific helper functions (URLs, API calls).
"""

import requests
from typing import Dict, Any, Optional
from urllib.parse import urlencode

__all__ = [
    "build_powerbi_report_url",
    "get_powerbi_access_token",
    "get_report_metadata",
]


def build_powerbi_report_url(
        workspace_id: str,
        report_id: str,
        params: Optional[Dict[str, Any]] = None,
) -> str:
    """Build Power BI report embed URL."""
    base_url = f"https://app.powerbi.com/groups/{workspace_id}/reports/{report_id}"

    if params:
        query_string = urlencode(params)
        base_url += f"?{query_string}"

    return base_url


def get_powerbi_access_token(
        client_id: str,
        client_secret: str,
        tenant_id: str,
        scope: str = "https://analysis.windows.net/powerbi/api/.default",
) -> str:
    """Get Power BI access token using client credentials flow."""
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()

    return response.json()["access_token"]


def get_report_metadata(
        access_token: str,
        workspace_id: str,
        report_id: str,
) -> Dict[str, Any]:
    """Get Power BI report metadata via REST API."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()
