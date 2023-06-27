import {Injectable} from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import {catchError, Observable, throwError} from 'rxjs';
import {AuthService} from "../services/auth.service";
import {NotificationService} from "../services/notification.service";
import {Router} from "@angular/router";

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService,
              private router: Router,
              private notificationService: NotificationService) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError(err => {
        if ([401, 403].includes(err.status) && this.authService.isLoggedIn()) {
          this.authService.logout();
          this.router.navigate(['/login-register']).then(() => {
            this.notificationService.showWarning("Session expired", "Your session has expired", "topRight");
          })
        }

        return throwError(() => err);
      }))
  }
}
