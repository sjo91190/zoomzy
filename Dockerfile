FROM python:latest
RUN apt-get update
RUN apt-get upgrade -y
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "zoomzy"]