import {Component, OnInit, ViewChild} from '@angular/core';
import {CredentialsFormComponent} from "../../forms/login/credentials-form/credentials-form.component";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{
  @ViewChild(CredentialsFormComponent) loginForm!: CredentialsFormComponent;

  constructor() {
  }

  ngOnInit(): void {
  }
}
