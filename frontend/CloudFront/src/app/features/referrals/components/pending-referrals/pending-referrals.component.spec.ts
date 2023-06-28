import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PendingReferralsComponent } from './pending-referrals.component';

describe('PendingReferralsComponent', () => {
  let component: PendingReferralsComponent;
  let fixture: ComponentFixture<PendingReferralsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PendingReferralsComponent]
    });
    fixture = TestBed.createComponent(PendingReferralsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
