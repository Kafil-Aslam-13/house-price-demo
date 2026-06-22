FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# train the model at build time
RUN python run_pipeline.py

# expose Streamlit's port — this is what HF Spaces makes public
EXPOSE 7860

# run FastAPI in background, Streamlit in foreground
CMD uvicorn api.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run app/streamlit_app.py --server.address 0.0.0.0 --server.port 7860