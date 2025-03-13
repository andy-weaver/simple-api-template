from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from mock_api.models import Request, Response
from mock_api.from_request import from_request

# This imports the model code, and should be replaced with something that exists
from some_other_but_yet_unknown_source import call_michaels_code

def get_app():
    app = FastAPI()

    # POST endpoint: Expects JSON body validated by ProcessRequest.
    @app.post("/score-risky-occupants", response_model=Response)
    async def process_post_endpoint(request: Request):
        try:
            results = await run_tasks_concurrently(tasks, request.value)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return ProcessResponse(results=results)

    # GET endpoint: Expects query parameters (converted to ProcessRequest via dependency injection).
    @app.get("/score-risky-occupants", response_model=Response)
    async def process_get_endpoint(request: Request = Depends()):
        try:
            results = await run_tasks_concurrently(tasks, request.value)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return ProcessResponse(results=results)

    return app