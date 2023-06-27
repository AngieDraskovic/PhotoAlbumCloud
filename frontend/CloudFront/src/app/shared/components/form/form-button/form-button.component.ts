import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormArray, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-form-button',
  templateUrl: './form-button.component.html',
  styleUrls: ['./form-button.component.css']
})
export class FormButtonComponent implements OnInit {
  @Input() form!: FormGroup | FormArray;
  @Input() buttonText!: string;
  @Output() onSubmit = new EventEmitter<void>();

  constructor() {
  }

  ngOnInit(): void {
  }

  submitForm() {
    if (this.form.valid) {
      this.onSubmit.emit();
    }
  }
}
