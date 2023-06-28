import {Component, Input, OnInit} from '@angular/core';
import {Invitation} from "../../models/invitation";

@Component({
  selector: 'app-pending-referral-row',
  templateUrl: './pending-referral-row.component.html',
  styleUrls: ['./pending-referral-row.component.css']
})
export class PendingReferralRowComponent implements OnInit {
  @Input() item: Invitation | null = null;
  @Input() acceptReferral!: (username: string) => void;
  @Input() declineReferral!: (username: string) => void;

  constructor() {
  }

  ngOnInit() {
  }

  getName(): string {
    if (!this.item) return '';
    return this.item.InvitedUser;
  }

  getStatus(): string {
    if (!this.item) return '';
    return this.item.Status;
  }

  acceptReferralClick() {
    if (!this.item) return;
    this.acceptReferral(this.item.InvitedUser);
  }

  declineReferralClick() {
    if (!this.item) return;
    this.declineReferral(this.item.InvitedUser);
  }
}
