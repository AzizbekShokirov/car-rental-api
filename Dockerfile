FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Run migrations and initialize data
RUN python manage.py migrate
RUN python manage.py initialize_rentprices

# Expose the port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]