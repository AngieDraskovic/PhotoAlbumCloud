import {Injectable} from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient, HttpErrorResponse, HttpParams} from "@angular/common/http";
import {catchError, Observable, throwError} from "rxjs";
import {UserRegistrationData} from "../../features/authentication/models/user-registration-data";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly apiUrl = `${environment.apiUrl}`;

  constructor(private http: HttpClient) {
  }

  registerUser(user: UserRegistrationData): Observable<any> {
    let api = `${this.apiUrl}/signup`;
    return this.http.post(api, user).pipe(catchError(this.handleError));
  }

  checkUsernameAvailability(username: string): Observable<any> {
    let api = `${this.apiUrl}/authentication/check_username_availability`;
    const httpOptions = {
      params: new HttpParams().set('username', username)
    };
    return this.http.get(api, httpOptions).pipe(catchError(this.handleError));
  }

  handleError(error: HttpErrorResponse) {
    return throwError(() => error);
  }
}
