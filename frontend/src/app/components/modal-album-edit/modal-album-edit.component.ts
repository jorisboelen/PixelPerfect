import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AlbumModel } from '../../models'

@Component({
  selector: 'app-modal-album-edit',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './modal-album-edit.component.html',
  styleUrl: './modal-album-edit.component.css'
})
export class ModalAlbumEditComponent {
  @Input() album!: AlbumModel;

  constructor(public activeModal: NgbActiveModal) {}
}
