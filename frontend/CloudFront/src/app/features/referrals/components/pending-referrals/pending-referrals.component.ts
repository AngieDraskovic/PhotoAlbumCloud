import {Component, OnInit} from '@angular/core';
import {Invitation} from "../../models/invitation";
import {ReferralService} from "../../services/referral.service";
import {NotificationService} from "../../../../core/services/notification.service";

@Component({
  selector: 'app-pending-referrals',
  templateUrl: './pending-referrals.component.html',
  styleUrls: ['./pending-referrals.component.css']
})
export class PendingReferralsComponent implements OnInit {
  pendingReferrals: Invitation[] = [];

  constructor(private referralService: ReferralService,
              private notificationService: NotificationService) {
  }


  ngOnInit(): void {
    this.refresh();
  }

  refresh() {
    this.fetchSharedFiles();
  }

  fetchSharedFiles() {
    this.referralService.getPendingInvitations().subscribe({
      next: (invitationResponse) => {
        this.pendingReferrals = invitationResponse.invitations;
      },
      error: (error) => {
        this.notificationService.showDefaultError("topRight");
      }
    });
  }

  acceptReferral(username: string) {
    this.referralService.acceptInvitation(username).subscribe({
      next: () => {
        this.refresh();
        this.notificationService.showSuccess("Referral accepted", "Referral accepted successfully", "topRight");
      },
      error: (error) => {
        this.notificationService.showDefaultError("topRight");
      }
    });
  }

  declineReferral(username: string) {
    this.referralService.declineInvitation(username).subscribe({
      next: () => {
        this.refresh();
        this.notificationService.showSuccess("Referral rejected", "Referral rejected successfully", "topRight");
      },
      error: (error) => {
        this.notificationService.showDefaultError("topRight");
      }
    });
  }
}
