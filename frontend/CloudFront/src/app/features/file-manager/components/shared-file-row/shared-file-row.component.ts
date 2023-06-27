import {Component, Input, OnInit} from '@angular/core';
import {SharedFile} from "../../models/shared-file";

@Component({
  selector: 'app-shared-file-row',
  templateUrl: './shared-file-row.component.html',
  styleUrls: ['./shared-file-row.component.css']
})
export class SharedFileRowComponent implements OnInit {
  @Input() item: SharedFile | null = null;
  @Input() downloadFile!: (fileName: string, sharedBy: string, extension: string) => void;

  constructor() {
  }

  ngOnInit() {
  }

  getItemType(): string {
    if (!this.item) return 'unknown';
    const fileType = this.item.file_type;
    if (fileType.startsWith('audio')) return 'audio';
    if (fileType.startsWith('video')) return 'video';
    if (fileType.startsWith('text') || fileType.startsWith('application')) return 'text';
    if (fileType.startsWith('image')) return 'image';
    return 'image';
  }

  getImageSrc(): string {
    const itemType = this.getItemType();
    return `assets/images/album/${itemType}.svg`;
  }

  getName(): string {
    if (!this.item) return '';
    const parts = this.item.file_name.split('/');
    return parts[parts.length - 1];
  }

  getShareDate(): string {
    if (!this.item) return '';
    return this.item.share_time;
  }

  getSharedBy(): string {
    if (!this.item) return '';
    return this.item.shared_by;
  }

  downloadFileClick() {
    if (!this.item) return;

    this.downloadFile(this.item.file_name, this.item.shared_by, this.item.file_type);
  }
}
