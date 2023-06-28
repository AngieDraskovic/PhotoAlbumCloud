import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PendingReferralRowComponent } from './pending-referral-row.component';

describe('PendingReferralRowComponent', () => {
  let component: PendingReferralRowComponent;
  let fixture: ComponentFixture<PendingReferralRowComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PendingReferralRowComponent]
    });
    fixture = TestBed.createComponent(PendingReferralRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
