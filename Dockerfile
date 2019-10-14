FROM python:3

ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ADD dash /app

EXPOSE 8050

ENTRYPOINT ["python"]
CMD ["app.py"]
