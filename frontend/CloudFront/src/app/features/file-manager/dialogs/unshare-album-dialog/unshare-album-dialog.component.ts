import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {AlbumService} from "../../services/album.service";
import {NotificationService} from "../../../../core/services/notification.service";

@Component({
  selector: 'app-unshare-album-dialog',
  templateUrl: './unshare-album-dialog.component.html',
  styleUrls: ['./unshare-album-dialog.component.css']
})
export class UnshareAlbumDialogComponent implements OnInit {
  protected readonly HTMLInputElement = HTMLInputElement;
  private readonly albumName: string = "";

  constructor(private dialogRef: MatDialogRef<UnshareAlbumDialogComponent>,
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
    this.albumService.unshareAlbum(this.albumName, username)
      .subscribe({
        next: () => {
          this.notificationService.showSuccess("Successfully unshared", "Album unshared successfully", "topRight")
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
