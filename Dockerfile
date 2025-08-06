FROM teamacimisai/django-mssql-base:latest

WORKDIR /app

# install dependencies
RUN pip install pip --upgrade

# Copy requirements.txt file
COPY requirements.txt .

# Install libraries from requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 8050
