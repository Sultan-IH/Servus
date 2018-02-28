FROM python:3


COPY requirements.txt /servus/
RUN pip install --no-cache-dir -r /servus/requirements.txt

COPY . /servus
WORKDIR /servus
CMD [ "python", "SERVICES/Scraping/main.py" ]