import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {NotificationService} from "../../../../../core/services/notification.service";
import {UserRegistrationDataService} from "../../../services/user-registration-data.service";
import {UserService} from "../../../../../core/services/user.service";
import {UserRegistrationData} from "../../../models/user-registration-data";
import {Router} from "@angular/router";
import {AccountData} from "../../../models/account-data";

@Component({
  selector: 'app-more-info-form',
  templateUrl: './more-info-form.component.html',
  styleUrls: ['./more-info-form.component.css']
})
export class MoreInfoFormComponent implements OnInit{
  allTextPattern = "[a-zA-Z][a-zA-Z]*";
  datePattern = "^[12][0-9]{3}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$";

  moreInfoForm = new FormGroup({
    name: new FormControl('', [Validators.required, Validators.pattern(this.allTextPattern), Validators.minLength(3)]),
    surname: new FormControl('', [Validators.required, Validators.pattern(this.allTextPattern), Validators.minLength(3)]),
    email: new FormControl('', [Validators.required, Validators.email]),
    dateOfBirth: new FormControl('', [Validators.required, Validators.pattern(this.datePattern)]),
  }, {});

  @Output() onBack = new EventEmitter<void>();
  @Output() onFormSubmit = new EventEmitter<void>();

  private formData: { isReferral: boolean, data: AccountData } | null = null;

  constructor(
    private notificationService: NotificationService,
    private registrationDataService: UserRegistrationDataService,
    private userService: UserService,
    private router: Router) {
  }

  ngOnInit(): void {
    this.registrationDataService.getRegistrationData().subscribe(data => {
      this.formData = data;
    });
  }

  navigateBack() {
    this.onBack.emit();
  }

  submitForm() {
    if (!this.moreInfoForm.valid || !this.formData) {
      return;
    }

    const user: UserRegistrationData = {
      first_name: this.moreInfoForm.get('name')?.value ?? '',
      last_name: this.moreInfoForm.get('surname')?.value ?? '',
      email: this.moreInfoForm.get('email')?.value ?? '',
      date_of_birth: this.moreInfoForm.get('dateOfBirth')?.value ?? '',
      username: this.formData.data.username,
      password: this.formData.data.password,
    };

    console.log(user);

    this.userService.registerUser(user).subscribe({
      next: () => {
        this.notificationService.showSuccess("Successful registration", "You have to confirm email that is sent to you", "topLeft");
      },
      error: (error) => {
        this.notificationService.showDefaultError("topLeft");
      }
    })
  }

  reset() {
    this.moreInfoForm.reset();
  }
}
