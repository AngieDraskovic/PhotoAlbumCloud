import { NgModule } from '@angular/core';
import {CommonModule, NgOptimizedImage} from '@angular/common';
import { FileFolderRowComponent } from './components/file-folder-row/file-folder-row.component';
import {MyAlbumsComponent} from "./components/my-albums/my-albums.component";
import {SharedModule} from "../../shared/shared.module";
import {MaterialModule} from "../../material/material.module";
import { CreateAlbumDialogComponent } from './dialogs/create-album-dialog/create-album-dialog.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { UploadFileDialogComponent } from './dialogs/upload-file-dialog/upload-file-dialog.component';
import { ShareFileDialogComponent } from './dialogs/share-file-dialog/share-file-dialog.component';
import { SharedWithMeComponent } from './components/shared-with-me/shared-with-me.component';
import { SharedFileRowComponent } from './components/shared-file-row/shared-file-row.component';
import { EditFileDialogComponent } from './dialogs/edit-file-dialog/edit-file-dialog.component';



@NgModule({
  declarations: [
    MyAlbumsComponent,
    FileFolderRowComponent,
    CreateAlbumDialogComponent,
    UploadFileDialogComponent,
    ShareFileDialogComponent,
    SharedWithMeComponent,
    SharedFileRowComponent,
    EditFileDialogComponent
  ],
  exports: [
    FileFolderRowComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    NgOptimizedImage,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule
  ]
})
export class FileManagerModule { }
