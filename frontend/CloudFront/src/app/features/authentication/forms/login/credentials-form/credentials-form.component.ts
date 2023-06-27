import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {NotificationService} from "../../../../../core/services/notification.service";
import {AuthService} from "../../../../../core/services/auth.service";
import {Credentials} from "../../../models/credentials";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login-form',
  templateUrl: './credentials-form.component.html',
  styleUrls: ['./credentials-form.component.css']
})
export class CredentialsFormComponent implements OnInit {
  loginForm = new FormGroup({
    email: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required])
  });

  @Output() onBack = new EventEmitter<void>();
  @Output() onLoginSubmit = new EventEmitter<void>();

  constructor(
    private authService: AuthService,
    private notificationService: NotificationService,
    private router: Router) {
  }

  ngOnInit(): void {
  }

  onFormSubmit() {
    if (this.loginForm.valid) {
      const credentials: Credentials = {
        username: this.loginForm.controls['email'].value ?? '',
        password: this.loginForm.controls['password'].value ?? ''
      };

      this.authService.loginUser(credentials).subscribe({
        next: () => {
          this.router.navigate(['home']);
        },
        error: (error) => {
          if (error.status == 401) {
            this.notificationService.showWarning("Invalid Credentials", "The credentials you entered are invalid!", 'topRight');
          } else if (error.status == 403) {
            this.notificationService.showWarning("Account not verified", "You did not verify your account!", 'topRight');
          } else {
            this.notificationService.showDefaultError('topRight');
          }
        }
      });
    }
  }

  reset() {
    this.loginForm.reset();
  }
}
