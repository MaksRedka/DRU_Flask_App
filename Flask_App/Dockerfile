FROM python:3.7

WORKDIR /Flask_App

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH='${PYTHONPATH}:/Flask_App'

COPY . .

EXPOSE 8000

CMD ["python", "./run.py"]