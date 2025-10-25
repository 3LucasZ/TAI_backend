import subprocess
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/toggleVideo")
def toggleVideo():
    subprocess.run(
        ["shortcuts", "run", "PlayPause"],
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
