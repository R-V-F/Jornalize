import { TestBed } from '@angular/core/testing';

import { NoticiasServiceService } from './noticias-service.service';

describe('NoticiasServiceService', () => {
  let service: NoticiasServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NoticiasServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
