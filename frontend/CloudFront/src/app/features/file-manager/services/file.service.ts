import {Injectable} from '@angular/core';
import {UploadData} from "../models/upload-data";
import {catchError, throwError} from "rxjs";
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {saveAs} from 'file-saver';
import {FileResponse} from "../models/file-response";
import {SharedWithResponse} from "../models/shared-with-response";
import {SharedFilesResponse} from "../models/shared-files-response";
import {UpdateFile} from "../models/update-file";
import {environment} from "../../../../environments/environment";
import * as FileSaver from 'file-saver';

@Injectable({
  providedIn: 'root'
})
export class FileService {
  private readonly apiUrl = `${environment.apiUrl}/file`;

  constructor(private http: HttpClient) {
  }

  getSharedFiles() {
    const api = `${this.apiUrl}/shared`;
    return this.http.get<SharedFilesResponse>(api).pipe(
      catchError(this.handleError)
    );
  }

  getSharedWith(albumName: string, fileName: string) {
    const api = `${this.apiUrl}/sharedwith`;
    const params = {
      album_name: albumName,
      file_name: fileName
    };

    return this.http.get<SharedWithResponse>(api, {params: params})
      .pipe(
        catchError(this.handleError)
      );
  }

  shareFile(albumName: string, fileName: string, shareWith: string) {
    const api = `${this.apiUrl}/share`;
    const body = {
      album_name: albumName,
      file_name: fileName,
      share_with: shareWith
    };

    return this.http.put(api, body)
      .pipe(
        catchError(this.handleError)
      );
  }

  revokeFileSharing(albumName: string, fileName: string, shareWith: string) {
    const api = `${this.apiUrl}/unshare`;
    const body = {
      album_name: albumName,
      file_name: fileName,
      unshare_with: shareWith
    };

    return this.http.put(api, body)
      .pipe(
        catchError(this.handleError)
      );
  }

  getFile(albumName: string, fileName: string) {
    const api = `${this.apiUrl}`;
    const params = {
      album_name: albumName,
      file_name: fileName
    };

    return this.http.get<FileResponse>(api, {params});
  }

  downloadFile(albumName: string, fileName: string, extension: string) {
    const api = `${this.apiUrl}/download`;
    const params = {
      album_name: albumName,
      file_name: fileName
    };

    this.http.get<{download_url: string}>(api, {params})
      .subscribe((response) => {
        const downloadUrl = response.download_url;
        this.downloadFromUrl(downloadUrl, fileName);
      });
  }

  downloadSharedFile(fileName: string, sharedBy: string, extension: string) {
    const api = `${this.apiUrl}/download`;
    let pathParts = fileName.split('/');
    let realFileName = pathParts.pop() ?? "";
    let albumName = pathParts.join('/');

    const params = {
      album_name: albumName,
      file_name: realFileName,
      shared_by: sharedBy,
    };

    this.http.get<{download_url: string}>(api, {params})
      .subscribe((response) => {
        const downloadUrl = response.download_url;
        this.downloadFromUrl(downloadUrl, realFileName);
      });
  }

  downloadFromUrl(url: string, fileName: string) {
    this.http.get(url, {responseType: 'blob'}).subscribe((response: Blob) => {
      saveAs(response, fileName);
    });
  }

  uploadFile(uploadData: UploadData) {
    const api = `${this.apiUrl}`;
    return this.http.post(api, uploadData)
      .pipe(
        catchError(this.handleError)
      );
  }

  updateFile(updateData: UpdateFile) {
    const api = `${this.apiUrl}`;
    return this.http.put(api, updateData)
      .pipe(
        catchError(this.handleError)
      );
  }

  deleteFile(albumName: string, fileName: string) {
    const api = `${this.apiUrl}`;
    return this.http.delete(api, {
      params: {album_name: albumName, file_name: fileName}
    }).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    return throwError(() => error);
  }
}
