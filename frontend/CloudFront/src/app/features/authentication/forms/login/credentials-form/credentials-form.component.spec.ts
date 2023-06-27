import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CredentialsFormComponent } from './credentials-form.component';

describe('LoginFormComponent', () => {
  let component: CredentialsFormComponent;
  let fixture: ComponentFixture<CredentialsFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CredentialsFormComponent]
    });
    fixture = TestBed.createComponent(CredentialsFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
