import {RouterModule, Routes} from "@angular/router";
import {NgModule} from "@angular/core";
import {HomeComponent} from "./components/home/home.component";
import {MyAlbumsComponent} from "../file-manager/components/my-albums/my-albums.component";
import {SharedWithMeComponent} from "../file-manager/components/shared-with-me/shared-with-me.component";
import {PendingReferralsComponent} from "../referrals/components/pending-referrals/pending-referrals.component";

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
    canActivate: [],
    children: [
      { path: '', redirectTo: 'my-albums', pathMatch: 'full' },
      { path: 'my-albums', component: MyAlbumsComponent },
      { path: 'shared-with-me', component: SharedWithMeComponent },
      { path: 'referrals', component: PendingReferralsComponent },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomeRoutingModule {
}
