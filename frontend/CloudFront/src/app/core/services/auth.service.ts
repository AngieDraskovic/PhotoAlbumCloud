import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {catchError, map, Observable, throwError} from "rxjs";
import {environment} from "../../../environments/environment";
import {StorageService} from "./storage.service";
import {Credentials} from "../../features/authentication/models/credentials";
import {Injectable} from "@angular/core";
import {AuthToken} from "../../features/authentication/models/auth-token";

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly apiUrl = `${environment.apiUrl}`;
  private tokenKey = 'auth_token';

  constructor(private http: HttpClient, private storageService: StorageService) {
  }

  loginUser(credentials: Credentials): Observable<AuthToken> {
    let api = `${this.apiUrl}/login`;
    return this.http.post<AuthToken>(api, credentials)
      .pipe(
        map(token => {
          this.setAuthToken(token.access_token);
          return token;
        }),
        catchError(this.handleError)
      );
  }

  isLoggedIn(): boolean {
    let authToken = this.getAuthToken();
    return authToken !== null;
  }

  logout() {
    this.storageService.clear();
  }

  getUsernameFromToken(): string | null {
    const token = this.getAuthToken();
    if (!token) {
      return null;
    }

    const tokenParts = token.split('.');
    const payloadEncoded = tokenParts[1];
    const payloadDecoded = atob(payloadEncoded);
    const payload = JSON.parse(payloadDecoded);
    return payload.username;
  }

  setAuthToken(token: string) {
    this.storageService.setItem(this.tokenKey, token);
  }

  getAuthToken() {
    return this.storageService.getItem<string>(this.tokenKey);
  }

  handleError(error: HttpErrorResponse) {
    return throwError(() => error);
  }
}
