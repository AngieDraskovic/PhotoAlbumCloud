import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormButtonComponent} from "./components/form/form-button/form-button.component";
import {FormFieldComponent} from "./components/form/form-field/form-field.component";
import {BackButtonComponent} from "./components/form/back-button/back-button.component";
import {ReactiveFormsModule} from "@angular/forms";
import {DateFormatPipe} from './pipes/date-format.pipe';


@NgModule({
  declarations: [
    FormButtonComponent,
    FormFieldComponent,
    BackButtonComponent,
    DateFormatPipe
  ],
  exports: [
    FormFieldComponent,
    FormButtonComponent,
    BackButtonComponent,
    DateFormatPipe
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
  ]
})
export class SharedModule {
}
