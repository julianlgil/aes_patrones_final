from fastapi import APIRouter
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient

from .schemas import InputMessage

router = APIRouter()


@router.post("/telegram/send_message")
async def send_message(message: InputMessage):
    api_id = "23499804"
    api_hash = "93dac6240ebeb6d1d8a530ecca8912bb"
    numeroTelefono = "+573178863279"
    nombreUsuarioTelegram = message.nombreUsuarioTelegram
    mensaje_envio = message.mensaje_envio
    clienteTelegram = TelegramClient("sesión", api_id, api_hash)
    async with clienteTelegram:
        await clienteTelegram.connect()
        if not await clienteTelegram.is_user_authorized():
            clienteTelegram.send_code_request(numeroTelefono)
        try:
            clienteTelegram.sign_in(numeroTelefono, "17353")
        except SessionPasswordNeededError:
            clienteTelegram.sign_in(numeroTelefono, input("Introduzca la contraseña: "))
        receptorNombre = await clienteTelegram.get_input_entity(nombreUsuarioTelegram)
        await clienteTelegram.send_message(receptorNombre, mensaje_envio)
        print(
            "Enviado mensaje a chat de Bot del receptor [{}] de Telegram".format(
                nombreUsuarioTelegram
            )
        )
        await clienteTelegram.disconnect()
    # clienteTelegram.loop.run_until_complete(main()) # Para que se ejecute la tarea anterior del método asíncrono
    print("Desconectando sesión de Telegram...")
    # await clienteTelegram.disconnect()
    print("Desconectado y fin del programa")

    return {"mensaje": "Mensaje enviado correctamente"}
