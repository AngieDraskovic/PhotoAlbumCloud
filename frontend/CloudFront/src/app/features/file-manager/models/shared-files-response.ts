import {SharedFile} from "./shared-file";

export interface SharedFilesResponse {
  message: string;
  shared_files: SharedFile[];
}
