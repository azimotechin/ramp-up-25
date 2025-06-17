#This file will contain instructions for Docker to build your publisher's image. It will:
    #Start from an official Python base image.
    #Copy your requirements.txt file into the image.
    #Run pip install to install the dependencies from requirements.txt.
    #Copy your publisher.py code into the image.
    #Specify the command to run when the container starts \
        #(e.g., uvicorn publisher:app --host 0.0.0.0 --port 8000).

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "publisher:app", "--host", "0.0.0.0", "--port", "8000"]