export interface UpdateFile {
  album_name: string;
  file_name: string;
  file_size: number,
  new_file_content_base64: string;
  description: string;
  tags: string[];
}
