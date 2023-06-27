import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FileFolderRowComponent } from './file-folder-row.component';

describe('FileFolderRowComponent', () => {
  let component: FileFolderRowComponent;
  let fixture: ComponentFixture<FileFolderRowComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FileFolderRowComponent]
    });
    fixture = TestBed.createComponent(FileFolderRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
