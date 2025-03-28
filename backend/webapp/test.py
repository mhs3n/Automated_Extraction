import os
import subprocess
import threading
import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from queue import Queue

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allow Angular frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow POST and OPTIONS
    allow_headers=["*"],  # Allow all headers
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Store the process and event to control the script
script_process = None
stop_event = threading.Event()
log_queue = Queue()  # Queue to store logs
DOCUMENTS_PATH = "/home/Ray/Desktop/Automated_extraction/pdf_downloads"


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

@app.get("/get-years")
def get_available_years():
    """Returns a list of years available in the documents folder."""
    if not os.path.exists(DOCUMENTS_PATH):
        return {"years": []}
    
    years = [d for d in os.listdir(DOCUMENTS_PATH) if os.path.isdir(os.path.join(DOCUMENTS_PATH, d))]
    return {"years": sorted(years)}

@app.get("/get-pdfs/{year}")
def get_pdfs_for_year(year: str):
    """Returns a list of PDFs available under the given year."""
    year_path = os.path.join(DOCUMENTS_PATH, year)
    
    if not os.path.exists(year_path):
        return {"error": "Year not found"}
    
    pdfs = [f for f in os.listdir(year_path) if f.endswith(".pdf")]
    return {"pdfs": pdfs}

@app.get("/view-pdf/{year}/{filename}")
def view_pdf(year: str, filename: str):
    """Serve PDFs for inline viewing instead of downloading"""
    pdf_path = os.path.join(DOCUMENTS_PATH, year, filename) 
    if not os.path.exists(pdf_path):
        return {"error": "File not found"}

    return FileResponse(pdf_path, media_type="application/pdf")
