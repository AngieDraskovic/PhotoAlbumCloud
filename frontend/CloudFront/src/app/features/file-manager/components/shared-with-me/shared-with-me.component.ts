import {Component, OnInit} from '@angular/core';
import {FileService} from "../../services/file.service";
import {SharedFile} from "../../models/shared-file";
import {NotificationService} from "../../../../core/services/notification.service";

@Component({
  selector: 'app-shared-with-me',
  templateUrl: './shared-with-me.component.html',
  styleUrls: ['./shared-with-me.component.css']
})
export class SharedWithMeComponent implements OnInit {
  constructor(private fileService: FileService,
              private notificationService: NotificationService) {
  }

  sharedFiles: SharedFile[] = [];

  ngOnInit(): void {
    this.refresh();
  }

  refresh() {
    this.fetchSharedFiles();
  }

  fetchSharedFiles() {
    this.fileService.getSharedFiles().subscribe({
      next: (sharedFileResponse) => {
        this.sharedFiles = sharedFileResponse.shared_files;
      },
      error: (error) => {
        this.notificationService.showDefaultError("topRight");
      }
    });
  }

  downloadFile(fileName: string, sharedBy: string, extension: string) {
    this.fileService.downloadSharedFile(fileName, sharedBy, extension);
  }
}
