FROM python:3.7

WORKDIR /Flask App

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH='${PYTHONPATH}:/Flask App'

COPY . .

CMD ["python", "./run.py"]