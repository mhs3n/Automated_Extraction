import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AboutComponent } from './about/about.component';
import { DatabaseComponent } from './database/database.component';
import { DocumentsComponent } from './documents/documents.component';
import { trigger, state, style, animate, transition } from '@angular/animations';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    AboutComponent,
    DatabaseComponent,
    DocumentsComponent
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  animations: [
    trigger('logoSlide', [
      state('initial', style({ left: '50%', transform: 'translateX(-50%)', top: '40px' })),
      state('active', style({ left: '0', transform: 'translateX(0)', top: '0' })),
      transition('initial <=> active', animate('0.5s ease-in-out'))
    ]),
    trigger('buttonFade', [
      state('visible', style({ opacity: 1, transform: 'translateY(0)' })),
      state('hidden', style({ opacity: 0, transform: 'translateY(-20px)' })),
      transition('visible <=> hidden', animate('0.3s ease-in-out'))
    ]),
    trigger('contentSlide', [
      state('hidden', style({ opacity: 0, transform: 'translateY(50px)' })),
      state('visible', style({ opacity: 1, transform: 'translateY(0)' })),
      transition('hidden <=> visible', animate('0.5s ease-in-out'))
    ]),
    trigger('backButtonFade', [
      state('hidden', style({ opacity: 0 })),
      state('visible', style({ opacity: 1 })),
      transition('hidden <=> visible', animate('0.3s ease-in-out'))
    ])
  ]
})
export class AppComponent {
  currentSection: string | null = null;
  logoState = 'initial';
  buttonState = 'visible';

  showSection(section: string | null) {
    this.currentSection = section;
    if (section) {
      this.logoState = 'active';
      this.buttonState = 'hidden';
    } else {
      this.logoState = 'initial';
      this.buttonState = 'visible';
    }
  }
}