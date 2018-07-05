FROM python:3.6
ADD . /usr/code
WORKDIR /usr/code
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]