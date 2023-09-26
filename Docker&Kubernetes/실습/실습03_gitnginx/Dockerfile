FROM ubuntu
RUN apt-get update && apt-get install -y git
RUN mkdir /myapp
WORKDIR /myapp
COPY cloner /myapp/
CMD [ "sh", "/myapp/cloner" ]