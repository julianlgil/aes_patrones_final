import os

import requests
from fastapi import HTTPException
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

CLIENTS_HOST = os.getenv('CLIENTS_HOST')


class Notification:

    def __init__(self, client_id):
        self.appID = '23499804'
        self.appAPIHash = '93dac6240ebeb6d1d8a530ecca8912bb'
        clients_url = f'{CLIENTS_HOST}{client_id}'
        client_response = requests.get(clients_url)
        if client_response.status_code != 200:
            raise HTTPException(status_code=client_response.status_code, detail=client_response.json())
        self.client = client_response.json()

    async def send_notification(self, bill_reference: str, amount: str):
        numeroTelefono = self.client.get('cellphone')
        client_name = f"{self.client.get('name')} {self.client.get('lastname')}"
        user_telegram = self.client.get('dane_code')
        mensaje_envio = ("Buen dia " + client_name + ". \nSe realizó el pago exitoso de su recibo: " + bill_reference +
                         " por un monto de: "+ amount + ' COP.')
        clienteTelegram = TelegramClient('sesión', self.appID, self.appAPIHash)
        async with clienteTelegram:
            await clienteTelegram.connect()
            if not await clienteTelegram.is_user_authorized():
                clienteTelegram.send_code_request(numeroTelefono)
            try:
                clienteTelegram.sign_in(numeroTelefono, '12354')
            except SessionPasswordNeededError:
                clienteTelegram.sign_in(numeroTelefono, '12354')
            receptorNombre = await clienteTelegram.get_input_entity(user_telegram)
            print("Enviando mensaje a chat de Bot del receptor de Telegram (usuario)...")
            await clienteTelegram.send_message(receptorNombre, mensaje_envio)
            print("Enviado mensaje a chat de Bot del receptor [{}] de Telegram".format(user_telegram))

            await clienteTelegram.disconnect()
