import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalAlbumEditComponent } from './modal-album-edit.component';

describe('ModalAlbumEditComponent', () => {
  let component: ModalAlbumEditComponent;
  let fixture: ComponentFixture<ModalAlbumEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalAlbumEditComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModalAlbumEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
