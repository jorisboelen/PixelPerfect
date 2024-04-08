import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalAlbumAddComponent } from './modal-album-add.component';

describe('ModalAlbumAddComponent', () => {
  let component: ModalAlbumAddComponent;
  let fixture: ComponentFixture<ModalAlbumAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalAlbumAddComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModalAlbumAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
