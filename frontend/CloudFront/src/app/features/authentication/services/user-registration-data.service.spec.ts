import { TestBed } from '@angular/core/testing';

import { UserRegistrationDataService } from './user-registration-data.service';

describe('UserRegistrationDataService', () => {
  let service: UserRegistrationDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UserRegistrationDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
