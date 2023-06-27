import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SharedFileRowComponent } from './shared-file-row.component';

describe('SharedFileRowComponent', () => {
  let component: SharedFileRowComponent;
  let fixture: ComponentFixture<SharedFileRowComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SharedFileRowComponent]
    });
    fixture = TestBed.createComponent(SharedFileRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
