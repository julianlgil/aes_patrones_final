from telethon.sync import TelegramClient

api_id = "23499804"
api_hash = "93dac6240ebeb6d1d8a530ecca8912bb"
phone_number = "+573178863279"

# Create a TelegramClient instance
client = TelegramClient("session_name", api_id, api_hash)

# Connect to the Telegram server
client.connect()

# Check if the user is not authorized
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input("Enter the code: "))

receptorNombre = client.get_input_entity("julianlgil")
client.send_message(receptorNombre, "cualquier cosa de mensaje_envio")
