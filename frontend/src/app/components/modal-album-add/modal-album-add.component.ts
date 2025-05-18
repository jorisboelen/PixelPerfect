import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AlbumModel } from '../../models'

@Component({
    selector: 'app-modal-album-add',
    imports: [FormsModule],
    templateUrl: './modal-album-add.component.html',
    styleUrl: './modal-album-add.component.css'
})
export class ModalAlbumAddComponent {
  @Input() album!: AlbumModel;

  constructor(public activeModal: NgbActiveModal) {}
}
