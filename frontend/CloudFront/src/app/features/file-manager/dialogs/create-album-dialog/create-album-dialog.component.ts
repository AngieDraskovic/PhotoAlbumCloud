import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {AlbumService} from "../../services/album.service";
import {NotificationService} from "../../../../core/services/notification.service";

@Component({
  selector: 'app-create-album-dialog',
  templateUrl: './create-album-dialog.component.html',
  styleUrls: ['./create-album-dialog.component.css']
})
export class CreateAlbumDialogComponent implements OnInit {
  private readonly currentPath: string = "";

  createAlbumForm = new FormGroup({
    name: new FormControl('', [Validators.required, Validators.pattern('^[a-zA-Z]*$')])
  });

  constructor(private dialogRef: MatDialogRef<CreateAlbumDialogComponent>,
              private albumService: AlbumService,
              private notificationService: NotificationService,
              @Inject(MAT_DIALOG_DATA) public data: any) {
    this.currentPath = data.currentPath;
    if (this.currentPath == "INITIAL") {
      this.currentPath = "";
    }
  }

  ngOnInit() {
  }

  cancel() {
    this.dialogRef.close(false);
  }

  create() {
    if (this.createAlbumForm.valid) {
      let albumName = this.createAlbumForm.controls['name'].value ?? '';
      if (this.currentPath != "") {
        albumName = this.currentPath + '/' + albumName;
      }

      this.albumService.createAlbum(albumName).subscribe({
        next: () => {
          this.dialogRef.close(true);
        },
        error: (error) => {
          if (error.status == 409) {
            this.notificationService.showWarning("Name already exists", "Album name already exists", "topRight");
          }
        }
      });
    }
  }
}
