import {RouterModule, Routes} from "@angular/router";
import {NgModule} from "@angular/core";
import {LoginRegisterComponent} from "./components/login-register/login-register.component";
import {authGuard} from "../../core/guards/auth.guard";

const routes: Routes = [
  {
    path: '',
    component: LoginRegisterComponent,
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthenticationRoutingModule {
}
