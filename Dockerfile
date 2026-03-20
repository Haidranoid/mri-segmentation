# -------- Stage 1: Build --------
FROM python:3.12-slim AS build

# Create working directory
WORKDIR /app

# Install compilation tools
RUN apt-get update && apt-get install -y build-essential

# Copy the requirements file
COPY requirements.txt .

# Download wheels from the requirements.txt
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

# -------- Stage 2: Runtime --------
#FROM python:3.12
FROM python:3.12-slim-trixie

WORKDIR /app

# Copy the wheels downloaded from build stage
COPY --from=build /wheels /wheels

# Install dependencies from wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]