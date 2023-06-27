export interface UploadData {
  album_name: string;
  file_name: string;
  file_type: string;
  file_size: number;
  description: string;
  tags: string[];
  file_content_base64: string;
}
