FROM python:3.7-alpine
RUN apk update && apk add bash
ADD ./server/ /app
COPY ./docker/wait-for-it.sh /app/wait-for-it.sh
WORKDIR /app
RUN pip install -r requirements.txt
VOLUME /app
# VOLUME /app/config
# EXPOSE 5000/tcp
CMD ["/app/wait-for-it.sh", "-t", "120", "mongo:27017", "--", "python", "manage.py", "runserver"]
# CMD ["/app/wait-for-it.sh", "-t", "120", "mongo:27017", "--", "python", "app/main.py"]
