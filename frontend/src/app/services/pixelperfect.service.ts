import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, repeat, of, tap, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { NotificationService } from './notification.service';
import { Album, Photo, User, NotificationLevel } from '../interfaces';
import { AlbumModel, UserLoginModel } from '../models';

@Injectable({
  providedIn: 'root'
})
export class PixelPerfectService {
  private apiBaseUrl = environment.mixmatchApiBaseUrl;
  private current_user?: User;

  constructor(private http: HttpClient, private notification: NotificationService, private router: Router) { }

  generateRefreshToken(seconds: number = 3600): number {
    return Math.floor(Date.now() / (seconds * 1000));
  }

  generateSize(): number {
    return Math.max(window.screen.width, window.screen.height);
  }

  getAlbums(): Observable<Album[]> {
    let apiUrl = this.apiBaseUrl + '/albums/';
    return this.http.get<Album[]>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getAlbum(album_id: number): Observable<Album> {
    let apiUrl = this.apiBaseUrl + '/albums/' + album_id;
    return this.http.get<Album>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getAlbumPhotos(album_id: number): Observable<Photo[]> {
    let apiUrl = this.apiBaseUrl + '/albums/' + album_id + '/photos';
    return this.http.get<Photo[]>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  addAlbumPhoto(album_id: number, file: File, formData: FormData = new FormData()): Observable<string> {
    let apiUrl = this.apiBaseUrl + '/albums/' + album_id + '/upload';
    formData.append("files", file, file.name);
    return this.http.post<string>(apiUrl, formData, {withCredentials: true}).pipe(
      tap(_ => this.handleEvent('Photo ' + file.name + ' uploaded')),
      catchError(this.handleError.bind(this))
    );
  }

  getPhotoImage(photo_id: number): Observable<Blob> {
    let apiUrl = this.apiBaseUrl + '/photos/' + photo_id + '/image?size=' + this.generateSize() + '&refresh=' + this.generateRefreshToken();
    return this.http.get(apiUrl, {withCredentials: true, responseType: "blob"}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getPhotoImageThumbnail(photo_id: number): Observable<Blob> {
    let apiUrl = this.apiBaseUrl + '/photos/' + photo_id + '/image?size=thumbnail&refresh=' + this.generateRefreshToken();
    return this.http.get(apiUrl, {withCredentials: true, responseType: "blob"}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  addAlbum(album: AlbumModel): Observable<AlbumModel> {
    let apiUrl = this.apiBaseUrl + '/albums/';
    return this.http.post<AlbumModel>(apiUrl, album, {withCredentials: true}).pipe(
      tap(_ => this.handleEvent('Album created')),
      catchError(this.handleError.bind(this))
    );
  }

  deleteAlbum(album_id: number): Observable<string> {
    let apiUrl = this.apiBaseUrl + '/albums/' + album_id;
    return this.http.delete<string>(apiUrl, {withCredentials: true}).pipe(
      tap(_ => this.handleEvent('Album removed')),
      catchError(this.handleError.bind(this))
    );
  }

  updateAlbum(album_id: number, album: AlbumModel): Observable<AlbumModel> {
    let apiUrl = this.apiBaseUrl + '/albums/' + album_id;
    return this.http.put<AlbumModel>(apiUrl, album, {withCredentials: true}).pipe(
      tap(_ => this.handleEvent('Album updated')),
      catchError(this.handleError.bind(this))
    );
  }

  updateAlbumCover(album_id: number, cover_photo_id: number): Observable<AlbumModel> {
    let apiUrl = this.apiBaseUrl + '/albums/' + album_id + '/cover?cover_photo_id=' + cover_photo_id;
    return this.http.put<AlbumModel>(apiUrl, {}, {withCredentials: true}).pipe(
      tap(_ => this.handleEvent('Album cover updated')),
      catchError(this.handleError.bind(this))
    );
  }

  deletePhoto(photo_id: number): Observable<string> {
    let apiUrl = this.apiBaseUrl + '/photos/' + photo_id;
    return this.http.delete<string>(apiUrl, {withCredentials: true}).pipe(
      tap(_ => this.handleEvent('Photo removed')),
      catchError(this.handleError.bind(this))
    );
  }

  getUserCurrent(): Observable<User> {
    let apiUrl = this.apiBaseUrl + '/users/me';
    return this.http.get<User>(apiUrl, {withCredentials: true}).pipe(
      tap(current_user => this.current_user = current_user),
      catchError(this.handleError.bind(this))
    );
  }

  isAdminUser(): boolean {
    if (this.current_user && this.current_user.is_admin){return true;}
    else { return false; }
  }

  login(user_login: UserLoginModel): Observable<string> {
    let apiUrl = this.apiBaseUrl + '/login';
    return this.http.post<string>(apiUrl, user_login, {withCredentials: true}).pipe(
      tap(_ => {this.getUserCurrent().subscribe(); this.router.navigateByUrl('')}),
      catchError(this.handleError.bind(this))
    );
  }

  logout(): Observable<string> {
    let apiUrl = this.apiBaseUrl + '/logout';
    return this.http.post<string>(apiUrl, {}, {withCredentials: true}).pipe(
      tap(_ => {this.current_user = undefined; this.router.navigateByUrl('/login')}),
      catchError(this.handleError.bind(this))
    );
  }

  private handleEvent(message: string): void {
    this.notification.addNotification(NotificationLevel.INFO, message)
  }

  private handleError(error: HttpErrorResponse) {
    let error_message = 'An error occurred: ' + error.message;
    if (error.status === 401){error_message = 'Incorrect username and/or password';}
    if (error.status === 403){error_message = 'Permission denied'; this.router.navigateByUrl('/login');}
    else {this.notification.addNotification(NotificationLevel.ERROR, error_message);}
    return throwError(() => new Error(error_message));
  }
}
