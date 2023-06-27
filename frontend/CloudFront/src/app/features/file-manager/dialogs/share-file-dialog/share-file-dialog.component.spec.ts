import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShareFileDialogComponent } from './share-file-dialog.component';

describe('ShareFileDialogComponent', () => {
  let component: ShareFileDialogComponent;
  let fixture: ComponentFixture<ShareFileDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ShareFileDialogComponent]
    });
    fixture = TestBed.createComponent(ShareFileDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
