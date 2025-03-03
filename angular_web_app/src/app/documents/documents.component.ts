import { Component, OnDestroy, ChangeDetectorRef, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-documents',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './documents.component.html',
  styleUrls: ['./documents.component.css']
})
export class DocumentsComponent implements OnDestroy {
  isUpdatingDocuments = false;
  years: string[] = [];
  selectedYear: string | null = null;
  pdfs: string[] = [];
  logs: string[] = [];
  baseUrl = 'http://localhost:8000';
  lastDownloaded: string = '';
  viewMode: 'default' | 'folders' = 'default';
  showLogBox = false;
  @ViewChild('logBox', { static: false }) logBox!: ElementRef; // Reference to log box
  private destroy$ = new Subject<void>();

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {
    this.fetchLastDownloaded();
  }

  toggleUpdateDocuments() {
    this.isUpdatingDocuments = !this.isUpdatingDocuments;
    const url = this.isUpdatingDocuments ? `${this.baseUrl}/run-script` : `${this.baseUrl}/stop-script`;
    this.http.post(url, {}).subscribe({
      next: (response: any) => {
        console.log(response.message);
        if (this.isUpdatingDocuments) {
          this.showLogBox = true;
          this.logs = [];
          this.streamLogs();
        } else {
          setTimeout(() => {
            this.showLogBox = false;
            this.logs = [];
            this.fetchLastDownloaded();
          }, 5000);
        }
      },
      error: (err) => console.error('Error toggling update:', err)
    });
  }

  streamLogs() {
    const eventSource = new EventSource(`${this.baseUrl}/stream-logs`);
    eventSource.onmessage = (event) => {
      const logLine = event.data.startsWith('data: ') ? event.data.slice(6) : event.data;
      this.logs.push(logLine);
      this.cdr.detectChanges();
      this.scrollToBottom(); // Scroll to bottom after each log
    };
    eventSource.onerror = () => {
      console.error('Log stream error');
      eventSource.close();
    };
    this.destroy$.subscribe(() => eventSource.close());
  }

  scrollToBottom() {
    if (this.logBox) {
      const element = this.logBox.nativeElement;
      element.scrollTop = element.scrollHeight; // Scroll to bottom
    }
  }

  uploadDocuments(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      const formData = new FormData();
      formData.append('file', file, file.name);
      this.http.post(`${this.baseUrl}/upload-pdf`, formData).subscribe({
        next: (response: any) => console.log(response.message),
        error: (err) => console.error('Upload error:', err)
      });
    }
  }

  fetchLastDownloaded() {
    this.http.get<{ filename: string }>(`${this.baseUrl}/last-downloaded`).subscribe({
      next: (response) => this.lastDownloaded = response.filename || 'No downloads yet',
      error: (err) => console.error('Error fetching last downloaded:', err)
    });
  }

  toggleViewDocuments() {
    if (this.viewMode === 'folders') {
      this.viewMode = 'default';
      this.selectedYear = null;
      this.pdfs = [];
      this.fetchLastDownloaded();
    } else {
      this.viewMode = 'folders';
      this.fetchYears();
    }
  }

  fetchYears() {
    this.http.get<{ years: string[] }>(`${this.baseUrl}/get-years`).subscribe({
      next: (response) => this.years = response.years,
      error: (err) => console.error('Error fetching years:', err)
    });
  }

  selectYear(year: string) {
    if (this.selectedYear === year) {
      this.selectedYear = null;
      this.pdfs = [];
    } else {
      this.selectedYear = year;
      this.http.get<{ pdfs: string[] }>(`${this.baseUrl}/get-pdfs/${year}`).subscribe({
        next: (response) => this.pdfs = response.pdfs,
        error: (err) => console.error('Error fetching PDFs:', err)
      });
    }
  }

  viewDocument(filename: string) {
    if (this.selectedYear) {
      window.open(`${this.baseUrl}/view-pdf/${this.selectedYear}/${filename}`, '_blank');
    }
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}