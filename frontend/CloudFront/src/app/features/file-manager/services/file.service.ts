import {Injectable} from '@angular/core';
import {UploadData} from "../models/upload-data";
import {catchError, Observable, throwError} from "rxjs";
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {saveAs} from 'file-saver';
import {FileResponse} from "../models/file-response";
import {SharedWithResponse} from "../models/shared-with-response";
import {SharedFilesResponse} from "../models/shared-files-response";
import {UpdateFile} from "../models/update-file";

@Injectable({
  providedIn: 'root'
})
export class FileService {
  private apiUrl = 'https://39f7siu2g1.execute-api.us-east-1.amazonaws.com/file';

  constructor(private http: HttpClient) {
  }

  getSharedFiles() {
    const api = `${this.apiUrl}/get-shared-files`;
    return this.http.get<SharedFilesResponse>(api).pipe(
      catchError(this.handleError)
    );
  }

  getSharedWith(albumName: string, fileName: string) {
    const api = `${this.apiUrl}/get-shared-with`;
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

    console.log(body);

    return this.http.put(api, body)
      .pipe(
        catchError(this.handleError)
      );
  }

  getFile(albumName: string, fileName: string) {
    const api = `${this.apiUrl}/get`;
    const params = {
      album_name: albumName,
      file_name: fileName
    };

    return this.http.get<FileResponse>(api, {params});
  }

  downloadFile(albumName: string, fileName: string, extension: string) {
    const api = `${this.apiUrl}/get`;
    const params = {
      album_name: albumName,
      file_name: fileName
    };

    this.http.get<FileResponse>(api, {params}).subscribe(response => {
      const data = response.file_content_base64;
      const byteCharacters = atob(data);
      const byteArrays = [];

      for (let offset = 0; offset < byteCharacters.length; offset += 512) {
        const slice = byteCharacters.slice(offset, offset + 512);
        const byteNumbers = new Array(slice.length);

        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
      }

      const blob = new Blob(byteArrays, {type: extension});

      saveAs(blob, fileName);
    });
  }

  downloadSharedFile(fileName: string, sharedBy: string, extension: string) {
    const api = `${this.apiUrl}/get`;
    let pathParts = fileName.split('/');
    let realFileName = pathParts.pop() ?? "";
    let albumName = pathParts.join('/');

    const params = {
      album_name: albumName,
      file_name: realFileName,
      shared_by: sharedBy,
    };

    this.http.get<FileResponse>(api, {params}).subscribe(response => {
      const data = response.file_content_base64;
      const byteCharacters = atob(data);
      const byteArrays = [];

      for (let offset = 0; offset < byteCharacters.length; offset += 512) {
        const slice = byteCharacters.slice(offset, offset + 512);
        const byteNumbers = new Array(slice.length);

        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
      }

      const blob = new Blob(byteArrays, {type: extension});

      saveAs(blob, realFileName);
    });
  }

  uploadFile(uploadData: UploadData) {
    const api = `${this.apiUrl}/create`;
    return this.http.post(api, uploadData)
      .pipe(
        catchError(this.handleError)
      );
  }

  updateFile(updateData: UpdateFile) {
    const api = `${this.apiUrl}/update`;
    return this.http.put(api, updateData)
      .pipe(
        catchError(this.handleError)
      );
  }

  deleteFile(albumName: string, fileName: string) {
    const api = `${this.apiUrl}/delete`;
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
