import { TestBed } from '@angular/core/testing';

import { PixelPerfectService } from './pixelperfect.service';

describe('PixelPerfectService', () => {
  let service: PixelPerfectService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PixelPerfectService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
