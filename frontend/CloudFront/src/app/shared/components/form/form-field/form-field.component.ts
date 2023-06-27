import {Component, Input, OnInit} from '@angular/core';
import {FormGroup} from "@angular/forms";

@Component({
  selector: 'app-form-field',
  templateUrl: './form-field.component.html',
  styleUrls: ['./form-field.component.css']
})
export class FormFieldComponent implements OnInit {
  @Input() formGroup!: FormGroup;
  @Input() controlName!: string;
  @Input() type!: string;
  @Input() icon!: string;
  @Input() placeholder!: string;
  @Input() errorMessages!: { [key: string]: string };
  @Input() disabled: boolean = false;

  constructor() {
  }

  ngOnInit(): void {
  }

  isInvalidAndTouched() {
    const control = this.formGroup.get(this.controlName);
    return control && control.touched && control.invalid;
  }

  getErrorMessage() {
    const control = this.formGroup.get(this.controlName);

    if (!control || !control.errors) {
      return null;
    }

    for (const errorName in control.errors) {
      if (control.errors.hasOwnProperty(errorName)) {
        if (this.errorMessages && this.errorMessages[errorName]) {
          return this.errorMessages[errorName];
        } else {
          return this.getDefaultErrorMessage(errorName, control.errors[errorName]);
        }
      }
    }

    return null;
  }

  getDefaultErrorMessage(errorName: string, errorValue: any): string | null {
    switch (errorName) {
      case 'required':
        return 'Input cannot be empty';
      case 'minlength':
        return `Minimum length is ${errorValue.requiredLength}`;
      case 'maxlength':
        return `Maximum length is ${errorValue.requiredLength}`;
      case 'email':
        return 'Invalid email address';
      default:
        return null;
    }
  }
}
