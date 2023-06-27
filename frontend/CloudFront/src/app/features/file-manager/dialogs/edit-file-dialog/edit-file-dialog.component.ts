import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {FileService} from "../../services/file.service";
import {NotificationService} from "../../../../core/services/notification.service";
import {UpdateFile} from "../../models/update-file";

@Component({
  selector: 'app-edit-file-dialog',
  templateUrl: './edit-file-dialog.component.html',
  styleUrls: ['./edit-file-dialog.component.css']
})
export class EditFileDialogComponent implements OnInit {
  private readonly currentPath: string = "";

  uploadFileForm = new FormGroup({
    name: new FormControl('', [Validators.required]),
    description: new FormControl('', [Validators.required]),
  });

  tags: string[] = [];
  maxTags = 5;

  file: File | null = null;
  fileContent: string | undefined = undefined;
  fileType : string = "";

  constructor(private dialogRef: MatDialogRef<EditFileDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any,
              private fileService: FileService,
              private notificationService: NotificationService) {
    this.currentPath = data.currentPath;
    if (this.currentPath == "INITIAL") {
      this.currentPath = "";
    }

    if (data.file) {
      this.uploadFileForm.patchValue({
        name: data.file.file_name,
        description: data.file.description,
      });

      this.tags = data.file.tags.slice(0, this.maxTags);
      this.fileType = data.file.file_type;

      const reader = new FileReader();
      reader.onload = () => {
        this.fileContent = reader.result?.toString();
      }
    }
  }

  ngOnInit() {
    this.getInitialFile();
  }

  cancel() {
    this.dialogRef.close(false);
  }

  getInitialFile() {
    const fileName = this.uploadFileForm.controls['name'].value ?? "";
    if (fileName == null || fileName == "") {
      return;
    }
    const splitFileName = fileName.split('/');
    const fileBaseName = splitFileName[splitFileName.length - 1];

    this.fileService.getFile(this.currentPath, fileBaseName).subscribe({
      next: (response) => {
        this.fileContent = response.file_content_base64;
      },
      error: (error) => {
        this.notificationService.showDefaultError('topRight');
      }
    })
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
      if (file.type != this.fileType) {
        this.notificationService.showWarning("Invalid file type", "File type must be the same as posted document", "topRight");
        return;
      }

      this.file = file;
      const reader = new FileReader();
      reader.onload = () => {
        this.fileContent = reader.result?.toString();
        if (this.fileContent != undefined) {
          this.fileContent = this.fileContent.split(',')[1];
        }
      }
      reader.readAsDataURL(file);
    }
  }

  create() {
    if (this.file && this.file.size > 2.5 * 1024 * 1024) {
      this.notificationService.showWarning("File too large", "Maximum size is 2.5 Mb", "topRight");
      return;
    }

    if (this.uploadFileForm.valid && this.fileContent) {
      const fileName = this.uploadFileForm.get('name')?.value ?? "";
      const updateFile: UpdateFile = {
        album_name: this.currentPath,
        file_name: fileName,
        description: this.uploadFileForm.get('description')?.value ?? "",
        tags: this.tags,
        new_file_content_base64: this.fileContent,
      };

      this.fileService.updateFile(updateFile).subscribe({
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
}
