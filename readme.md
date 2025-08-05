ollama run mistral

uvicorn hackrx_fastapi_llm:app --reload

http://127.0.0.1:8000/docs


curl -X POST http://127.0.0.1:8000/hackrx/run -H "Content-Type: application/json" -H "Authorization: Bearer 6890cfc475e4b61cf6b049684a7c7fa65ebb88696d672f1a9ce7d86f901bdbb8" -d @payload.json

curl -X POST "http://127.0.0.1:8000/hackrx/run" ^
 -H "Content-Type: application/json" ^
 -H "Authorization: Bearer 6890cfc475e4b61cf6b049684a7c7fa65ebb88696d672f1a9ce7d86f901bdbb8" ^
 -d @payload.json
