#!/bin/bash
pip install -r requirements.txt
python -m uvicorn backend:app --host 0.0.0.0 --port $PORT 