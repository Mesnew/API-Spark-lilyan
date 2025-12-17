"""
Middleware d'authentification OAuth2
Valide les tokens auprès du serveur OAuth2
"""
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import httpx
import os

security = HTTPBearer()

# URL du serveur OAuth2
OAUTH2_URL = os.getenv("OAUTH2_URL", "http://localhost:3000")


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Vérifie le token OAuth2 en appelant l'API OAuth2

    Args:
        credentials: Credentials Bearer token

    Returns:
        dict: Informations du token validé

    Raises:
        HTTPException: Si le token est invalide
    """
    token = credentials.credentials

    try:
        # Appeler l'endpoint /secure de l'API OAuth2 pour valider le token
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{OAUTH2_URL}/secure",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5.0
            )

            if response.status_code == 200:
                # Token valide
                return response.json()
            elif response.status_code == 401:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="OAuth2 server error"
                )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"OAuth2 server unavailable: {str(e)}"
        )


async def get_current_user(token_data: dict = Depends(verify_token)) -> dict:
    """
    Récupère les informations de l'utilisateur courant

    Args:
        token_data: Données du token validé

    Returns:
        dict: Informations utilisateur
    """
    return token_data.get("user", {})


# Dépendance optionnelle pour les endpoints publics
async def optional_verify_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Optional[dict]:
    """
    Vérifie le token OAuth2 de manière optionnelle
    Retourne None si pas de token
    """
    if credentials is None:
        return None

    return await verify_token(credentials)
