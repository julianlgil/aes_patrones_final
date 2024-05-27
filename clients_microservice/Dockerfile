FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
    
WORKDIR /app
COPY  requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# CMD ["uvicorn", "crud_example.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
