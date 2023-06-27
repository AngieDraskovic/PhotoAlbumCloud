import {Injectable} from '@angular/core';
import {BehaviorSubject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class UserRegistrationDataService {
  private formData = new BehaviorSubject<{ isReferral: boolean, data: any } | null>(null);

  setRegistrationData(data: { isReferral: boolean, data: any }) {
    this.formData.next(data);
  }

  getRegistrationData() {
    return this.formData.asObservable();
  }
}
