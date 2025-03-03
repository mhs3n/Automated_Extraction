import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideHttpClient } from '@angular/common/http'; // Correct import

bootstrapApplication(AppComponent, {
  providers: [
    provideAnimations(),
    provideHttpClient() // Provides HttpClient app-wide
  ]
})
  .catch(err => console.error(err));