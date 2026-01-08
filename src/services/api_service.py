from typing import Dict, List, Optional, Any
from config.settings import settings    
from config.logging_config import setup_logger
import httpx

logger = setup_logger(__name__)

class ApiService:
    
    def __init__(self) -> None:
        self._api_url = settings.API_URL
        
    async def _execute_request(self, 
                         method: str,
                         endpoint: str,
                         headers: Optional[dict],
                         data: Optional[dict],
                         timeout: float = 10.0) -> Any:
        logger.info("Init request")
        url = f"{self._api_url}/{endpoint}"
        logger.info(f"Request to {url}")
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.request(
                    method=method.upper(),
                    url=url,
                    json=data if method.upper() == 'POST' else None,
                    params=data if method.upper() == 'GET' else None,
                    headers=headers
                )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise Exception(f"HTTP error occurred: {http_err}")
    
    async def login(self, username: str, password: str) -> Optional[Dict] | None:
        data = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        
        response = await self._execute_request(
            method='POST',
            endpoint='auth/signin',
            headers=headers,
            data=data,
            timeout=30.0
        )
        
        return response        
    
    async def get_historical_by_user(self, access_token: str) -> Optional[Dict] | None:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = await self._execute_request(
            method='GET',
            endpoint='historico',
            headers=headers,
            data={},
            timeout=300.0,
        )
        return response
            
    async def get_incomes_by_user(self, access_token: str) -> List[Dict]: # type: ignore
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = await self._execute_request(
            method='GET',
            endpoint='ingreso-egreso/ingresos-egresos-usuario',
            headers=headers,
            data={},
            timeout=500.0
        )
        return response if response else []
    
    async def get_dollars_transactions_by_user(self, access_token: str) -> List[Dict]:  # type: ignore
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = await self._execute_request(
            method='GET',
            endpoint='compradolar/listar-operaciones',
            headers=headers,
            data={},
            timeout=500.0
        )
        return response if response else []

api_service = ApiService()