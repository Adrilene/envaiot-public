FROM python:3.10-alpine

WORKDIR /Simulator

COPY ./requirements.txt /Simulator
RUN pip install -r requirements.txt

COPY . /Simulator

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["docker-run.py"]
