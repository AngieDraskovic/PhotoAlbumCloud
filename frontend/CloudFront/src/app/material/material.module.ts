import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {MatIconModule} from "@angular/material/icon";
import {MatMenuModule} from "@angular/material/menu";
import {MatButtonModule} from "@angular/material/button";
import {MatDialog, MatDialogModule} from "@angular/material/dialog";


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MatIconModule,
    MatMenuModule,
    MatButtonModule,
    MatDialogModule
  ],
  exports: [
    MatIconModule,
    MatMenuModule,
    MatButtonModule,
    MatDialogModule
  ]
})
export class MaterialModule {
}
