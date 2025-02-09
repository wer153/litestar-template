import uvicorn
from litestar_project.app import create_app


def run():
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000) 