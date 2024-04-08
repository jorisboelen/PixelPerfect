import { Routes } from '@angular/router';
import { MainComponent } from './pages/main/main.component';
import { AlbumComponent } from './pages/album/album.component';
import { LoginComponent } from './pages/login/login.component';

export const routes: Routes = [
  { path: '', component: MainComponent },
  { path: 'album/:id', component: AlbumComponent },
  { path: 'login', component: LoginComponent },
];
