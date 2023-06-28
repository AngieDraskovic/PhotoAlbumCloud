import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShareAlbumDialogComponent } from './share-album-dialog.component';

describe('ShareAlbumDialogComponent', () => {
  let component: ShareAlbumDialogComponent;
  let fixture: ComponentFixture<ShareAlbumDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ShareAlbumDialogComponent]
    });
    fixture = TestBed.createComponent(ShareAlbumDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
