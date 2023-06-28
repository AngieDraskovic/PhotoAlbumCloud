import {Injectable} from '@angular/core';
import {environment} from "../../../../environments/environment";
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {catchError, Observable, throwError} from "rxjs";
import {InvitationResponse} from "../models/invitation-response";

@Injectable({
  providedIn: 'root'
})
export class ReferralService {
  private readonly apiUrl = `${environment.apiUrl}/invitations`;

  constructor(private http: HttpClient) {
  }

  public getPendingInvitations(): Observable<InvitationResponse> {
    let api = `${this.apiUrl}/get-pending-invitations`;

    return this.http.get<InvitationResponse>(api).pipe(
      catchError(this.handleError)
    );
  }

  public acceptInvitation(invited_username: string): Observable<any> {
    let api = `${this.apiUrl}/accept`;

    return this.http.put(api, { invited_username }).pipe(
      catchError(this.handleError)
    );
  }

  public declineInvitation(invited_username: string): Observable<any> {
    let api = `${this.apiUrl}/decline`;

    return this.http.put(api, { invited_username }).pipe(
      catchError(this.handleError)
    );;
  }

  handleError(error: HttpErrorResponse) {
    return throwError(() => error);
  }
}
