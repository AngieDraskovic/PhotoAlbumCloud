import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {FileService} from "../../services/file.service";
import {NotificationService} from "../../../../core/services/notification.service";

@Component({
  selector: 'app-share-file-dialog',
  templateUrl: './share-file-dialog.component.html',
  styleUrls: ['./share-file-dialog.component.css']
})
export class ShareFileDialogComponent implements OnInit{
  private readonly currentPath: string = "";
  private readonly fileName: string = "";
  sharedWith: string[] = [];

  constructor(private dialogRef: MatDialogRef<ShareFileDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any,
              private fileService: FileService,
              private notificationService: NotificationService) {
    this.currentPath = data.currentPath;
    if (this.currentPath == "INITIAL") {
      this.currentPath = "";
    }

    this.fileName = data.fileName;
  }

  ngOnInit() {
    this.refresh();
  }

  onEnter(event: any) {
    const username = event.target.value;

    if (username != '') {
      this.shareFile(username);
    }
  }

  shareFile(username:string) {
    this.fileService.shareFile(this.currentPath, this.fileName, username)
      .subscribe({
        next: () => {
          this.notificationService.showSuccess("Successfully shared", "File shared successfully", "topRight")
          this.refresh();
        },
        error: (error) => {
          if (error.status == 400) {
            this.notificationService.showWarning("File already shared", "File already shared with user", "topRight");
          } else if (error.status == 404) {
            this.notificationService.showWarning("User not found", "User is not found.", "topRight");
          } else {
            this.notificationService.showDefaultError("topRight");
          }
        }
      });
  }

  revokeFileSharing(username:string) {
    this.fileService.revokeFileSharing(this.currentPath, this.fileName, username)
      .subscribe({
        next: () => {
          this.notificationService.showSuccess("Successfully revoked sharing", "File share revoked successfully", "topRight")
          this.refresh();
        },
        error: (error) => {
          if (error.status == 400) {
            this.notificationService.showWarning("File already shared", "File already shared with user", "topRight");
          } else if (error.status == 404) {
            this.notificationService.showWarning("No shared file found", "No shared file found.", "topRight");
          } else {
            this.notificationService.showDefaultError("topRight");
          }
        }
      });
  }

  refresh() {
    this.fileService.getSharedWith(this.currentPath, this.fileName)
      .subscribe({
        next: (response) => {
          this.sharedWith = response.shared_with;
        },
        error: (error) => {
          this.notificationService.showDefaultError("topRight");
        }
      });
  }

  protected readonly HTMLInputElement = HTMLInputElement;
}
