import { NgModule } from '@angular/core';
import {CommonModule, NgOptimizedImage} from '@angular/common';
import { LoginRegisterComponent } from './components/login-register/login-register.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { CredentialsFormComponent } from './forms/login/credentials-form/credentials-form.component';
import {SharedModule} from "../../shared/shared.module";
import {ReactiveFormsModule} from "@angular/forms";
import {AuthenticationRoutingModule} from "./authentication-routing.module";
import { AccountCreationFormComponent } from './forms/registration/account-creation-form/account-creation-form.component';
import { MoreInfoFormComponent } from './forms/registration/more-info-form/more-info-form.component';


@NgModule({
  declarations: [
    LoginRegisterComponent,
    LoginComponent,
    RegisterComponent,
    CredentialsFormComponent,
    AccountCreationFormComponent,
    MoreInfoFormComponent
  ],
  imports: [
    CommonModule,
    AuthenticationRoutingModule,
    NgOptimizedImage,
    ReactiveFormsModule,
    SharedModule
  ]
})
export class AuthenticationModule { }
