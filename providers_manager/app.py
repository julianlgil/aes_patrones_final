import os

import requests
from fastapi import FastAPI, HTTPException

from providers_manager.schemas import Provider, ProviderCreate

app = FastAPI()

# Assuming the provider service is running at this address
PROVIDERS_HOST = os.getenv('PROVIDERS_HOST')
ACCOUNTS_HOST = os.getenv('ACCOUNTS_HOST')


@app.post("/provider/", response_model=Provider)
async def create_provider(provider: ProviderCreate):
    accounts_url = f'{ACCOUNTS_HOST}{provider.account_id}/client/{provider.client_id}'
    account_response = requests.get(accounts_url)
    if account_response.status_code != 200:
        raise HTTPException(status_code=account_response.status_code, detail=account_response.json())
    response = requests.post(PROVIDERS_HOST, json=provider.dict())
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())


# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}
