import json
import os

import requests
from fastapi import HTTPException

CLIENTS_HOST = os.getenv("CLIENTS_HOST")


class Notification:
    def __init__(self, client_id):
        self.appID = "23499804"
        self.appAPIHash = "93dac6240ebeb6d1d8a530ecca8912bb"
        clients_url = f"{CLIENTS_HOST}{client_id}"
        client_response = requests.get(clients_url)
        if client_response.status_code != 200:
            raise HTTPException(
                status_code=client_response.status_code, detail=client_response.json()
            )
        self.client = client_response.json()

    def send_notification(self, bill_reference: str, amount: str):
        client_name = f"{self.client.get('name')} {self.client.get('last_name')}"
        user_telegram = self.client.get("dane_code")
        mensaje_envio = (
            "Buen dia "
            + client_name
            + ". \nSe realizó el pago exitoso de su recibo: "
            + bill_reference
            + " por un monto de: "
            + amount
            + " COP."
        )

        url = "http://telegram_api:8023/telegram/send_message"

        payload = json.dumps(
            {"nombreUsuarioTelegram": f"{user_telegram}", "mensaje_envio": f"{mensaje_envio}"}
        )
        headers = {
            "Content-Type": "application/json",
            "Cookie": "csrftoken=izpn1IwitshtEXNYIPcRCeZtXDEKmW5e",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
