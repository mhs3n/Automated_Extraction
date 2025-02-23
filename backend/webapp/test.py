from fastapi import FastAPI
from fastapi.responses import JSONResponse
import subprocess
import sys

app = FastAPI()

@app.post("/run-script")
async def run_script():
    try:
        # Run your script using subprocess
        process = subprocess.Popen(
            [sys.executable, "/home/Ray/Desktop/Automated_extraction/backend/Downloader/pdf_downloader.py"],  # Make sure the script path is correct
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Capture the output of the script
        stdout, stderr = process.communicate()

        # Check if there's any error
        if process.returncode != 0:
            return JSONResponse(content={"error": stderr}, status_code=500)

        return JSONResponse(content={"message": "Script ran successfully", "output": stdout}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
