# Backend 

* To start the server: `kill -9 $(lsof -t -i:8000) 2>/dev/null; uvicorn backend.main:app --reload`