import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {catchError, Observable, throwError} from "rxjs";
import {Album} from "../models/album";
import {environment} from "../../../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class AlbumService {
  private readonly apiUrl = `${environment.apiUrl}/album`;

  constructor(private http: HttpClient) {
  }

  shareAlbum(albumName: string, shareWith: string) {
    const api = `${this.apiUrl}/share`;
    const payload = {
      album_name: albumName,
      share_with: shareWith
    };

    console.log(payload);

    return this.http.put(api, payload)
      .pipe(
        catchError(this.handleError)
      );
  }

  unshareAlbum(albumName: string, unshareWith: string) {
    const api = `${this.apiUrl}/unshare`;
    const payload = {
      album_name: albumName,
      unshare_with: unshareWith
    };

    return this.http.put(api, payload)
      .pipe(
        catchError(this.handleError)
      );
  }

  createAlbum(albumName: string) {
    const api = `${this.apiUrl}`;
    const payload = {
      album_name: albumName
    };

    return this.http.post(api, payload)
      .pipe(
        catchError(this.handleError)
      );
  }

  getAlbum(albumName: string): Observable<Album> {
    const api = `${this.apiUrl}`;

    return this.http.get<Album>(api, {
      params: {album_name: albumName}
    }).pipe(
      catchError(this.handleError)
    );
  }

  deleteAlbum(albumName: string) {
    const api = `${this.apiUrl}`;
    return this.http.delete(api, {
      params: {album_name: albumName}
    }).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    return throwError(() => error);
  }
}
