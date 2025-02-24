import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  message = '';
  logs: string[] = [];

  constructor(private http: HttpClient) {}

  // Trigger the script (POST request)
  executeScript() {
    this.http.post<{ message?: string; error?: string }>('http://localhost:8000/run-script', {})
      .subscribe(response => {
        this.message = response.message || response.error || 'Unknown response';
      }, error => {
        this.message = 'Error running script';
      });
  }
  

  // Connect to the log stream via SSE (Server-Sent Events)
  startLogStream() {
    const eventSource = new EventSource('http://localhost:8000/stream-logs');
    
    eventSource.onmessage = (event) => {
      const newLog = event.data as string;
      this.logs.push(newLog);
    };

    eventSource.onerror = (error) => {
      console.error('Error with SSE stream', error);
    };
  }

  // Stop the script (POST request)
  stopScript() {
    this.http.post<{ message?: string }>('http://localhost:8000/stop-script', {})
      .subscribe(response => {
        this.message = response.message || 'Unknown response';
      }, error => {
        this.message = 'Error stopping script';
      });
  }
}
