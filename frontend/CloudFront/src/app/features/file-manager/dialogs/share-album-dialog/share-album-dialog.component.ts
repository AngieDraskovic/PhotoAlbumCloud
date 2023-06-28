import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {FileService} from "../../services/file.service";
import {NotificationService} from "../../../../core/services/notification.service";
import {AlbumService} from "../../services/album.service";

@Component({
  selector: 'app-share-album-dialog',
  templateUrl: './share-album-dialog.component.html',
  styleUrls: ['./share-album-dialog.component.css']
})
export class ShareAlbumDialogComponent {
  protected readonly HTMLInputElement = HTMLInputElement;
  private readonly albumName: string = "";

  constructor(private dialogRef: MatDialogRef<ShareAlbumDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any,
              private albumService: AlbumService,
              private notificationService: NotificationService) {
    this.albumName = data.albumName;
  }

  ngOnInit() {
  }

  onEnter(event: any) {
    const username = event.target.value;

    if (username != '') {
      this.shareAlbum(username);
    }
  }

  shareAlbum(username:string) {
    this.albumService.shareAlbum(this.albumName, username)
      .subscribe({
        next: () => {
          this.notificationService.showSuccess("Successfully shared", "Album shared successfully", "topRight")
        },
        error: (error) => {
          if (error.status == 400) {
            this.notificationService.showWarning("Album already shared", "File already shared with user", "topRight");
          } else if (error.status == 404) {
            this.notificationService.showWarning("User not found", "User is not found.", "topRight");
          } else {
            this.notificationService.showDefaultError("topRight");
          }
        }
      });
  }
}
