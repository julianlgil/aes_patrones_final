from sqlmodel import SQLModel


class InputMessage(SQLModel):
    nombreUsuarioTelegram: str
    mensaje_envio: str
