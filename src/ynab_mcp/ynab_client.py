from typing import Any, Optional
import aiohttp
from pydantic import BaseModel

class YNABError(Exception):
    """Base exception for YNAB API errors"""
    def __init__(self, message: str, status: Optional[int] = None, detail: Optional[str] = None):
        self.message = message
        self.status = status
        self.detail = detail
        super().__init__(message)

class YNABResponse(BaseModel):
    """Base model for YNAB API responses"""
    data: dict[str, Any]

class YNABClient:
    """
    YNAB API client for making authenticated requests to the YNAB API.
    
    Args:
        api_key (str): Your YNAB API key
        
    Example:
        ```python
        client = YNABClient("your-api-key")
        await client.connect()
        try:
            user = await client.get_user()
            print(f"Hello {user['user']['name']}!")
        finally:
            await client.close()
        ```
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.ynab.com/v1"
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def connect(self) -> None:
        """Initialize the HTTP session"""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )
            
    async def close(self) -> None:
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Make an authenticated request to the YNAB API
        
        Args:
            method (str): HTTP method (GET, POST, etc)
            endpoint (str): API endpoint (e.g. /user)
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            dict: Parsed JSON response
            
        Raises:
            YNABError: If the API request fails
        """
        if not self.session:
            raise YNABError("Client not connected. Call connect() first.")
            
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with self.session.request(method, url, **kwargs) as response:
                if response.status == 200:
                    return await response.json()
                    
                error_body = await response.text()
                raise YNABError(
                    f"API request failed: {error_body}",
                    status=response.status,
                    detail=error_body
                )
                
        except aiohttp.ClientError as e:
            raise YNABError(f"Request failed: {str(e)}")
            
    async def get_user(self) -> dict:
        """
        Get authenticated user info
        
        Returns:
            dict: User information
            
        Example response:
            {
                "data": {
                    "user": {
                        "id": "...",
                        "name": "John Doe"
                    }
                }
            }
        """
        return await self._request("GET", "/user")
        
    async def list_budgets(self) -> dict:
        """
        List budgets for the authenticated user
        
        Returns:
            dict: List of budgets
            
        Example response:
            {
                "data": {
                    "budgets": [
                        {
                            "id": "...", 
                            "name": "My Budget",
                            "last_modified_on": "2024-04-19"
                        }
                    ]
                }
            }
        """
        return await self._request("GET", "/budgets")
        
    async def get_budget(self, budget_id: str) -> dict:
        """
        Get a single budget by id
        
        Args:
            budget_id (str): The id of the budget to fetch
            
        Returns:
            dict: Budget details
            
        Example response:
            {
                "data": {
                    "budget": {
                        "id": "...",
                        "name": "My Budget",
                        "last_modified_on": "2024-04-19",
                        "currency_format": {
                            "iso_code": "USD"
                        }
                    }
                }
            }
        """
        return await self._request("GET", f"/budgets/{budget_id}")
        
    async def get_budget_settings(self, budget_id: str) -> dict:
        """
        Get settings for a budget
        
        Args:
            budget_id (str): The id of the budget
            
        Returns:
            dict: Budget settings
            
        Example response:
            {
                "data": {
                    "settings": {
                        "date_format": {
                            "format": "MM/DD/YYYY"
                        },
                        "currency_format": {
                            "iso_code": "USD",
                            "example_format": "$1,234.56"
                        }
                    }
                }
            }
        """
        return await self._request("GET", f"/budgets/{budget_id}/settings")
