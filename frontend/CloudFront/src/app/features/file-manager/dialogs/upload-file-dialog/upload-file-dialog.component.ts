import {Component, Inject, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {AlbumService} from "../../services/album.service";
import {NotificationService} from "../../../../core/services/notification.service";
import {UploadData} from "../../models/upload-data";
import {FileService} from "../../services/file.service";

@Component({
  selector: 'app-upload-file-dialog',
  templateUrl: './upload-file-dialog.component.html',
  styleUrls: ['./upload-file-dialog.component.css']
})
export class UploadFileDialogComponent implements OnInit{
  private readonly currentPath: string = "";

  uploadFileForm = new FormGroup({
    name: new FormControl('', [Validators.required, Validators.pattern('^[a-zA-Z]*$')]),
    description: new FormControl('', [Validators.required]),
  });

  tags: string[] = [];
  maxTags = 5;

  file: File | null = null;
  fileContent: string | undefined = undefined;

  constructor(private dialogRef: MatDialogRef<UploadFileDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any,
              private fileService: FileService,
              private notificationService: NotificationService) {
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
    if (this.file && this.file.size > 2.5 * 1024 * 1024) {
      this.notificationService.showWarning("File too large", "Maximum size is 2.5 Mb", "topRight");
      return;
    }

    if (this.uploadFileForm.valid && this.file && this.fileContent) {
      const extension = this.file.name.split('.').pop();
      const fileName = this.uploadFileForm.get('name')?.value ?? "";

      const uploadData: UploadData = {
        album_name: this.currentPath,
        file_name: `${fileName}.${extension}`,
        file_type: this.file.type,
        file_size: Math.floor(this.file.size / 1024),
        description: this.uploadFileForm.get('description')?.value ?? "",
        tags: this.tags,
        file_content_base64: this.fileContent.split(',')[1],
      };

      this.fileService.uploadFile(uploadData).subscribe({
        next: () => {
          this.dialogRef.close(true);
        },
        error: (error) => {
          if (error.status == 409) {
            this.notificationService.showWarning("Name already used", "File name already used", "topRight");
          }
        }
      });
    }
  }

  addTag(tag: string) {
    const cleanedTag = tag.replace(/\s/g, '').replace(/\s[^a-zA-Z0-9]/g, "");
    if (this.tags.length < this.maxTags && cleanedTag !== '') {
      this.tags.push(cleanedTag);
    }
  }

  removeTag(index: number) {
    this.tags.splice(index, 1);
  }

  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement)?.files?.[0];
    if (file) {
      this.file = file;
      const reader = new FileReader();
      reader.onload = () => {
        this.fileContent = reader.result?.toString();
      }
      reader.readAsDataURL(file);
    }
  }
}
