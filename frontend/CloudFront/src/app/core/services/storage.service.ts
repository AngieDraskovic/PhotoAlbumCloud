import {Injectable} from "@angular/core";
@Injectable({
  providedIn: 'root',
})
export class StorageService {
  private storage: Storage;

  constructor() {
    this.storage = localStorage;
  }

  setItem(key: string, value: any): void {
    this.storage.setItem(key, JSON.stringify(value));
  }

  getItem<T>(key: string): T | null {
    const item = this.storage.getItem(key);
    return item ? JSON.parse(item) : null;
  }

  removeItem(key: string): void {
    this.storage.removeItem(key);
  }

  clear(): void {
    this.storage.clear();
  }
}
