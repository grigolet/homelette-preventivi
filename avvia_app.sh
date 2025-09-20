#!/bin/bash

# Script per avviare l'app Streamlit per i preventivi catering

cd /home/grigolet/cernbox/personal/code/homelette-preventivi

echo "🍽️ Avvio app Preventivi Catering..."
echo "L'app sarà disponibile su: http://localhost:8501"
echo "Premi Ctrl+C per fermare l'app"
echo ""

# Attiva l'ambiente virtuale e avvia Streamlit
source .venv/bin/activate
streamlit run preventivi_app.py --server.port 8501 --server.address 0.0.0.0
