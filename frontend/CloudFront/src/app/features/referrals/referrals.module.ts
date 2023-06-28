import {NgModule} from '@angular/core';
import {CommonModule, NgOptimizedImage} from '@angular/common';
import {PendingReferralsComponent} from './components/pending-referrals/pending-referrals.component';
import {PendingReferralRowComponent} from './components/pending-referral-row/pending-referral-row.component';
import {MaterialModule} from "../../material/material.module";


@NgModule({
  declarations: [
    PendingReferralRowComponent,
    PendingReferralsComponent,
  ],
  imports: [
    CommonModule,
    NgOptimizedImage,
    MaterialModule
  ]
})
export class ReferralsModule {
}
