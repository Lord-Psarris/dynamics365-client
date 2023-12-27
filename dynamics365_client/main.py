from pydantic import EmailStr
from typing import Optional

import fast_azure_client
import requests



class MicrosoftServicesClient:
    """
    Microsoft Services Client for interacting with Microsoft Dynamics 365 APIs.
    """

    def __init__(self, environment_url: str, access_token: Optional[str] = None,
                 client_id: Optional[str] = None, client_secret: Optional[str] = None,
                 tenant_id: Optional[str] = None, email: Optional[EmailStr] = None,
                 password: Optional[str] = None, disable_token_refresh: Optional[bool] = False):
        """
        Initializes the MicrosoftServicesClient.

        :param environment_url: The URL of the Dynamics 365 environment.
        :param access_token: Access token for authentication.
        :param client_id: Client ID for authentication.
        :param client_secret: Client secret for authentication.
        :param tenant_id: Tenant ID for authentication.
        :param email: User email for authentication.
        :param password: User password for authentication.
        :param disable_token_refresh: Whether to disable token refresh.
        """
        self.disable_token_refresh = disable_token_refresh
        self.environment_url = environment_url
        self.client_secret = client_secret
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.email = email
        self.password = password
        self.access_token = access_token

    def get(self, item: str, item_id: str = None) -> dict:
        """
        Sends a GET request to the Dynamics 365 API.

        :param item: The item to retrieve.
        :param item_id: The ID of the item if applicable.
        :return: The response data.
        """
        if item_id:
            item = f'{item}({item_id})'

        return self._make_request(item)

    def create(self, item: str, payload: dict) -> dict:
        """
        Sends a POST request to create an item in the Dynamics 365 API.

        :param item: The item to create.
        :param payload: The data to include in the request payload.
        :return: The response data.
        """
        return self._make_request(item, method="post", payload=payload)

    def update(self, item: str, item_id: str, payload: dict) -> dict:
        """
        Sends a PATCH request to update an item in the Dynamics 365 API.

        :param item: The item to update.
        :param item_id: The ID of the item to update.
        :param payload: The data to include in the request payload.
        :return: The response data.
        """
        return self._make_request(f'{item}({item_id})', method="patch", payload=payload)

    def delete(self, item: str, item_id: str) -> dict:
        """
        Sends a DELETE request to delete an item from the Dynamics 365 API.

        :param item: The item to delete.
        :param item_id: The ID of the item to delete.
        :return: The response data.
        """
        return self._make_request(f'{item}({item_id})', method="delete")

    def _make_request(self, path: str, method: str = "get", payload: dict = None,
                      headers: dict = None) -> dict:
        """
        Internal method to make HTTP requests to the Dynamics 365 API.

        :param path: The API path to request.
        :param method: The HTTP method (default is "get").
        :param payload: The payload data for POST or PATCH requests.
        :param headers: Additional headers for the request.
        :return: The response data.
        """
        # Generate access token
        if not self.disable_token_refresh:
            access_token = self._generate_user_token()
        else:
            access_token = self.access_token

        # Update headers
        headers.update({'Authorization': access_token})

        # Generate URL
        url = self._generate_base_url(path)

        # Make request
        if method == "get":
            response = requests.get(url, headers=headers)
        else:
            response = requests.request(method, url, json=payload, headers=headers)

        # TODO: implement better error handling
        response.raise_for_status()

        try:
            json_response = response.json()

            # Handle 201 response
        except requests.exceptions.JSONDecodeError:
            json_response = {"value": "request successful"}

        return json_response.get("value", json_response)

    def _generate_base_url(self, item: str) -> str:
        """
        Internal method to generate the base URL for API requests.

        :param item: The item to append to the URL.
        :return: The complete URL.
        """
        url = f"{self.environment_url}api/data/v9.0/{item}"
        return url

    def _generate_user_token(self, return_auth_url: bool = False) -> str:
        """
        Internal method to generate the user access token.

        :param return_auth_url: Whether to return the URL for granting consent.
        :return: The access token or auth URL.
        """
        # Setup auth client
        scopes = [f"{self.environment_url}user_impersonation"]
        client = fast_azure_client.AuthClient(self.client_id, self.client_secret, self.tenant_id,
                                              scopes=scopes, mode="b2c",
                                              authority=f"https://login.microsoftonline.com/organizations")

        # Return URL for granting consent
        if return_auth_url:
            return client.generate_auth_url()

        # Setup email password token
        token = client.authenticate_email_password(self.email, self.password)
        return token