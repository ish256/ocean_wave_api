# use latest python image 
FROM python:3.7.2-slim

#set working directory (makes folder in container and cd's into it)
WORKDIR /app

# Copy the current directory (on host machine) contents into the container at working directory
COPY . /app

# pip install all python dependencies in the requirements file 
RUN pip --no-cache-dir install -r /app/requirements.txt

#make a port available to the world outside this container 
EXPOSE 5000

# ENTRYPOINT allows us to specify the default executable to run on startup
ENTRYPOINT ["python"]

# CMD sets default arguements to executable but can be overwritten when using docker run
CMD ["app.py"]