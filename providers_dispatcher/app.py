from fastapi import FastAPI, HTTPException

from providers_dispatcher.dispatcher import Dispatcher

app = FastAPI()

# Definimos el cliente HTTP
client = httpx.Client()

@app.get("/providers/invoice/{invoice_reference}")
async def consume_api(invoice_reference: str):
    try:
        dispatcher = Dispatcher()
        provider_id = invoice_reference[0:3]
        json_data = {
            "invoice_reference": invoice_reference
        }
        dispatcher.do_request(provider_id, 'get_invoice', json_data)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Retornamos la respuesta de la API externa
    return response.json()


@app.post("/providers/payment_invoice")
async def consume_api(endpoint: str):
    try:
        # Realizamos una solicitud GET a la API externa
        response = client.get(endpoint)
        response.raise_for_status()  # Verifica si hubo algún error en la solicitud
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Retornamos la respuesta de la API externa
    return response.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)