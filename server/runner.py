import os
import uvicorn
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

os.environ["ENV"] = "debug"

if __name__ == "__main__":
    from server.api.main import app


    @app.get("/index")
    def read_main():
        return FileResponse("../client/static/index.html")


    app.mount("/static", StaticFiles(directory="../client/static"), name="static")
    app.mount("/js", StaticFiles(directory="../client/static/js"), name="js")
    app.mount("/css", StaticFiles(directory="../client/static/css"), name="css")
    uvicorn.run(app, port=5001)
