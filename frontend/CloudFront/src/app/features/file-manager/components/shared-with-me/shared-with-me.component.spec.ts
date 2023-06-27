import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SharedWithMeComponent } from './shared-with-me.component';

describe('SharedWithMeComponent', () => {
  let component: SharedWithMeComponent;
  let fixture: ComponentFixture<SharedWithMeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SharedWithMeComponent]
    });
    fixture = TestBed.createComponent(SharedWithMeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
