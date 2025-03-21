import subprocess
import os

# Lancer FastAPI en arrière-plan
subprocess.Popen(["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"])

# Lancer Streamlit
os.system("streamlit run modules/dashboard.py --server.port 8501")