import uvicorn
from litestar_project.app import create_app
from litestar_project.settings import server_settings

def run():
    app = create_app()
    uvicorn.run(app, host=server_settings.host, port=server_settings.port)
