# 
FROM python:3.12

COPY --from=ghcr.io/multi-py/python-uvicorn:py3.12-slim-LATEST /usr/local/lib/python3.12/site-packages/* /usr/local/lib/python3.12/site-packages/
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
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8060"]