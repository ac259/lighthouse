# Backend 

* To start the server: `kill -9 $(lsof -t -i:8000) 2>/dev/null; uvicorn backend.main:app --reload`

* To hit the endpoint: `curl -X POST "http://localhost:8000/api/analyze-hate-speech" -H "Content-Type: application/json" -d '{"text": "hate"}'`

* To get the list of all the endpoints: `http://localhost:8000/docs`