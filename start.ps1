Start-Process powershell -ArgumentList "cd backend; python -m uvicorn app.main:app --reload"
Start-Process powershell -ArgumentList "cd frontend; npm run dev"
