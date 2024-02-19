# 
FROM python:3.13.0a3-bookworm

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
#ENV FORWARDED_ALLOW_IPS=*
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--reload", "--host", "0.0.0.0", "--port", "80"]
