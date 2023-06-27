import {Component, OnInit, ViewChild} from '@angular/core';
import {
  AccountCreationFormComponent
} from "../../forms/registration/account-creation-form/account-creation-form.component";

enum RegisterStep {
  AccountCreationForm,
  MoreInfoForm
}

enum AnimationType {
  SLIDE_IN_LEFT = "slide-in-left",
  SLIDE_IN_RIGHT = "slide-in-right"
}

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  protected readonly RegisterStep = RegisterStep;

  @ViewChild(AccountCreationFormComponent) accountCreationForm!: AccountCreationFormComponent;

  animationType: AnimationType = AnimationType.SLIDE_IN_RIGHT;
  currentStep: RegisterStep = RegisterStep.AccountCreationForm;

  constructor() {
  }

  ngOnInit(): void {
  }

  nextStep() {
    this.animationType = AnimationType.SLIDE_IN_RIGHT;
    this.currentStep = RegisterStep.MoreInfoForm;
  }

  onBack() {
    this.animationType = AnimationType.SLIDE_IN_LEFT;
    this.currentStep = RegisterStep.AccountCreationForm;
  }
}
