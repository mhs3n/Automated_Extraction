import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-database',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './database.component.html',
  styleUrls: ['./database.component.css']
})
export class DatabaseComponent {
  companies: any[] = [];
  baseUrl = '/api';

  constructor(private http: HttpClient) {
    this.fetchDatabaseData();
  }

  fetchDatabaseData() {
    this.http.get<any[]>(`${this.baseUrl}/get-database-data`).subscribe({
      next: (response) => {
        this.companies = response.map(company => ({
          Company: company.company_name,
          Founders: company.founders,
          Location: company.location,
          Capital: company.capital,
          Contact: company.contact,
          News: company.news
        }));
      },
      error: (err) => console.error('Error fetching database data:', err)
    });
  }
}