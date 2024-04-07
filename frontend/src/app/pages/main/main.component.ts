import { Component } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { RouterLink } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ModalAlbumAddComponent } from '../../components/modal-album-add/modal-album-add.component';
import { ModalAlbumEditComponent } from '../../components/modal-album-edit/modal-album-edit.component';
import { ModalDeleteConfirmationComponent } from '../../components/modal-delete-confirmation/modal-delete-confirmation.component';
import { NavbarComponent } from '../../components/navbar/navbar.component';
import { PixelPerfectService } from '../../services/pixelperfect.service';
import { Album } from '../../interfaces';
import { AlbumModel } from '../../models';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [ NavbarComponent, NgFor, NgIf, RouterLink ],
  templateUrl: './main.component.html',
  styleUrl: './main.component.css'
})
export class MainComponent {
  album_list?: Album[];
  album_cover_list: {[photo_id: string]: SafeUrl} = {};

  constructor(private pixelperfectService: PixelPerfectService, private sanitizer: DomSanitizer, private modalService: NgbModal) {}

  ngOnInit(): void {
    this.getAlbumList();
  }

  openAlbumAddModal(): void {
    const album = new AlbumModel();
    const modal = this.modalService.open(ModalAlbumAddComponent, {});
    modal.componentInstance.album = album;
    modal.result.then(
      (result) => {this.addAlbum(album)},
      (reason) => {},
    );
  }

  openAlbumDeleteModal(album: Album): void {
    const modal = this.modalService.open(ModalDeleteConfirmationComponent, {});
    modal.componentInstance.modal_title = album.name;
    modal.result.then(
      (result) => {this.deleteAlbum(album)},
      (reason) => {},
    );
  }

  openAlbumEditModal(album: Album): void {
    const modal = this.modalService.open(ModalAlbumEditComponent, {});
    modal.componentInstance.album = album;
    modal.result.then(
      (result) => {this.updateAlbum(album)},
      (reason) => {},
    );
  }

  addAlbum(album: AlbumModel): void {
    this.pixelperfectService.addAlbum(album).subscribe((album) => this.getAlbumList());
  }

  updateAlbum(album: Album): void {
    this.pixelperfectService.updateAlbum(album.id, album).subscribe((album) => this.getAlbumList());
  }

  getAlbumList(): void {
    this.pixelperfectService.getAlbums().subscribe((album_list) => {
      this.album_list = album_list;
      for (let album of this.album_list) {
        this.getAlbumCover(album);
      }
    });
  }

  getAlbumCover(album: Album): void {
    if(album.cover_photo){
      this.pixelperfectService.getPhotoImageThumbnail(album.cover_photo.id).subscribe((photo_image) => {
        if(album.cover_photo && album.cover_photo.id){
          let photo_image_url = URL.createObjectURL(photo_image);
          this.album_cover_list[album.cover_photo.id] = this.sanitizer.bypassSecurityTrustUrl(photo_image_url);
        }
      })
    }
  }

  deleteAlbum(album: Album) {
    this.pixelperfectService.deleteAlbum(album.id).subscribe((album) => this.getAlbumList());
  }

  isAdminUser(): boolean {
    return this.pixelperfectService.isAdminUser();
  }
}
