import {RouterModule, Routes} from "@angular/router";
import {NgModule} from "@angular/core";
import {loggedInGuard} from "./core/guards/logged-in.guard";
import {authGuard} from "./core/guards/auth.guard";

const routes: Routes = [
  {
    path: '',
    redirectTo: 'login-register',
    pathMatch: 'full'
  },
  {
    path: 'login-register',
    loadChildren: () => import('./features/authentication/authentication.module').then(m => m.AuthenticationModule),
    canActivate: [loggedInGuard]
  },
  {
    path: 'home',
    loadChildren: () => import('./features/home/home.module').then(m => m.HomeModule),
    canActivate: [authGuard]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
