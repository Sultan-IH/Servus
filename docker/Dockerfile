FROM python:3


COPY requirements.txt /servus/
RUN pip install --no-cache-dir -r /servus/requirements.txt

COPY . /servus
WORKDIR /servus


EXPOSE 4555
CMD [ "python","-m","Scraping.main.py" ]