# Stage 1: Build environment
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv

# Copy only dependency definitions
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment in /app/.venv
# The --frozen flag ensures we use the exact versions in uv.lock
# The --no-dev flag excludes development dependencies
RUN uv sync --frozen --no-dev

# Stage 2: Runtime environment
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Make sure the virtualenv's binaries take precedence
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 5001

# Command to run the application
CMD ["python", "run.py"]
