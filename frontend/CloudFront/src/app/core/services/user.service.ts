import {Injectable} from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient, HttpErrorResponse, HttpParams} from "@angular/common/http";
import {catchError, Observable, throwError} from "rxjs";
import {UserRegistrationData} from "../../features/authentication/models/user-registration-data";
import {UserReferralRegistrationData} from "../../features/authentication/models/user-referral-registration-data";

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

  registerUserWithReferral(user: UserReferralRegistrationData): Observable<any> {
    let api = `${this.apiUrl}/signup`;
    return this.http.post(api, user).pipe(catchError(this.handleError));
  }

  checkUsernameAvailability(username: string): Observable<boolean> {
    let api = `${this.apiUrl}/check_username_availability`;
    const httpOptions = {
      params: new HttpParams().set('username', username)
    };
    return this.http.get<boolean>(api, httpOptions).pipe(catchError(this.handleError));
  }

  handleError(error: HttpErrorResponse) {
    return throwError(() => error);
  }
}
