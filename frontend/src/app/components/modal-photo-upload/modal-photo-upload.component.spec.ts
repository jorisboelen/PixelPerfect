import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalPhotoUploadComponent } from './modal-photo-upload.component';

describe('ModalPhotoUploadComponent', () => {
  let component: ModalPhotoUploadComponent;
  let fixture: ComponentFixture<ModalPhotoUploadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalPhotoUploadComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModalPhotoUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
