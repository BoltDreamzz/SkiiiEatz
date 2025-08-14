# Step 1: Use an official Python runtime as a parent image
FROM python:3.13

# Step 2: Set the working directory inside the container
WORKDIR /SkiiiEatz

# Step 3: Copy the current directory contents into the container
COPY . /SkiiiEatz

# Step 4: Install any needed packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Migrate the database and collect static files
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput --clear

# Step 6: Expose port 8000 for the web service
EXPOSE 8000

# Step 7: Set environment config for Django settings
ENV DJANGO_SETTINGS_MODULE=config.settings

# Step 8: Command to run the web application using gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]