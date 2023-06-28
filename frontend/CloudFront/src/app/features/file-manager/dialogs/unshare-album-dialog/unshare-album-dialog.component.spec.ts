import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnshareAlbumDialogComponent } from './unshare-album-dialog.component';

describe('UnshareAlbumDialogComponent', () => {
  let component: UnshareAlbumDialogComponent;
  let fixture: ComponentFixture<UnshareAlbumDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [UnshareAlbumDialogComponent]
    });
    fixture = TestBed.createComponent(UnshareAlbumDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
