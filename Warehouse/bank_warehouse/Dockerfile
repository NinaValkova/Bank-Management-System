FROM apache/airflow:3.0.0

# Switch to airflow user (default)
USER airflow

# Install extra Python packages via built-in AIRFLOW__CORE__ENABLE_XCOM_PICKLING
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
