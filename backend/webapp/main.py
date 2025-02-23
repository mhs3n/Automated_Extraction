import os
import subprocess
import threading
import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from queue import Queue

app = FastAPI()



# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Store the process and event to control the script
script_process = None
stop_event = threading.Event()
log_queue = Queue()  # Queue to store logs

@app.get("/")
def serve_html():
    return FileResponse("templates/index.html")

@app.post("/run-script")
def start_script():
    """Start the script in a background thread and begin streaming logs."""
    global script_process, stop_event
    if script_process and script_process.poll() is None:
        return {"message": "Script is already running."}

    logging.info("Script execution started.")
    stop_event.clear()

    # Set the environment variable to disable buffering (unbuffered output)
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    # Start the script in a new thread
    script_process = subprocess.Popen(
        ['python3', '/home/Ray/Desktop/Automated_extraction/backend/Downloader/pdf_downloader.py'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True,
        bufsize=1,  # Line-buffered output for real-time streaming
        env=env  # Pass the unbuffered environment variable
    )

    # Start a background thread to handle log streaming
    threading.Thread(target=stream_logs, daemon=True).start()

    return {"message": "Script started"}

@app.get("/last-downloaded")
def get_last_downloaded():
    """Reads the last downloaded document from last_downloaded.txt."""
    file_path = "/home/Ray/Desktop/Automated_extraction/backend/Downloader/last_downloaded.txt"
    try:
        with open(file_path, "r") as f:
            last_file = f.read().strip()
        return {"filename": last_file}
    except FileNotFoundError:
        return {"filename": "No downloads found"}

@app.post("/stop-script")
def stop_script():
    """Stop the running script."""
    global script_process, stop_event
    if script_process and script_process.poll() is None:
        stop_event.set()  # Trigger the stop event
        script_process.terminate()  # Terminate the running script
        script_process = None
        return {"message": "Script stopped"}
    return {"message": "No script is running."}

def stream_logs():
    """Stream logs from the script's output in real-time."""
    global script_process, log_queue
    try:
        if script_process:
            # Read stdout line by line using iter()
            for line in iter(script_process.stdout.readline, ''):
                if line:
                    log_queue.put(f"INFO: {line.strip()}")

            # Read stderr line by line using iter()
            for line in iter(script_process.stderr.readline, ''):
                if line:
                    log_queue.put(f"ERROR: {line.strip()}")

    except Exception as e:
        logging.error(f"Error during log streaming: {str(e)}")


@app.get("/stream-logs")
def stream_logs_endpoint():
    """Streaming response to send logs to the frontend."""
    def log_stream():
        """Generator to continuously stream logs to the frontend."""
        global log_queue
        while True:
            log = log_queue.get()  # Blocking call, waits until there's a log
            yield f"data: {log}\n\n"
            log_queue.task_done()  # Mark the log as processed

    return StreamingResponse(log_stream(), media_type="text/event-stream")


# --- New Routes for Documents ---
@app.get("/documents")
def serve_documents():
    return HTMLResponse(open("templates/documents.html").read())

@app.get("/documents/{path:path}")
def list_files(path: str = ""):
    base_path = "/home/Ray/Desktop/Automated_extraction/pdf_downloads"
    full_path = os.path.join(base_path, path)
    
    if not os.path.exists(full_path):
        return {"error": "Path does not exist"}

    # List directories and files
    directories = []
    files = []
    for entry in os.listdir(full_path):
        entry_path = os.path.join(full_path, entry)
        if os.path.isdir(entry_path):
            directories.append(entry)
        elif entry.endswith(".pdf"):
            files.append(entry)

    return {"directories": directories, "files": files}

@app.get("/download/{year}/{filename}")
def download_file(year: str, filename: str):
    file_path = f"/home/Ray/Desktop/Automated_extraction/pdf_downloads/{year}/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
