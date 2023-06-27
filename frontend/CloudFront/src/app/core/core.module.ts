import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HTTP_INTERCEPTORS} from "@angular/common/http";
import {AuthInterceptor} from "./interceptors/auth.interceptor";
import {NgToastModule} from "ng-angular-popup";
import {ErrorInterceptor} from "./interceptors/error.interceptor";
import {SpinnerInterceptor} from "./interceptors/spinner.interceptor";


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    NgToastModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: SpinnerInterceptor,
      multi: true
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ErrorInterceptor,
      multi: true
    },
  ]
})
export class CoreModule {
}
