import { Component } from '@angular/core';
import { NgClass, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'app-modal-photo-upload',
    imports: [NgClass, NgIf],
    templateUrl: './modal-photo-upload.component.html',
    styleUrl: './modal-photo-upload.component.css'
})
export class ModalPhotoUploadComponent {
  upload_error?: string;

  constructor(public activeModal: NgbActiveModal) {}

  upload(result: any): void {
    if (result.target.files.length > 100) {
      this.upload_error = 'Too many files selected. Select a maximum of 100 files.';
    } else {
      this.activeModal.close(result);
    }
  }
}
