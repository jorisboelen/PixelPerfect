import { Component, inject, TemplateRef, ViewChild } from '@angular/core';
import { DatePipe, NgFor, NgIf } from '@angular/common';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { NgbCarousel, NgbCarouselModule, NgbModal, NgbOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { PixelPerfectService } from '../../services/pixelperfect.service';
import { ModalDeleteConfirmationComponent } from '../../components/modal-delete-confirmation/modal-delete-confirmation.component';
import { ModalPhotoUploadComponent } from '../../components/modal-photo-upload/modal-photo-upload.component';
import { NavbarComponent } from '../../components/navbar/navbar.component';
import { Album, Photo } from '../../interfaces';

@Component({
  selector: 'app-album',
  standalone: true,
  imports: [ DatePipe, NavbarComponent, NgFor, NgIf, NgbCarouselModule, RouterLink ],
  templateUrl: './album.component.html',
  styleUrl: './album.component.css'
})
export class AlbumComponent {
  album?: Album;
  photo_list?: Photo[];
  photo_thumbnail_list: {[photo_id: string]: SafeUrl} = {};
  photo_image_list: {[photo_id: string]: SafeUrl} = {};
  photo_image_thumbnail_list: {[photo_id: string]: SafeUrl} = {};
  photo_selected?: Photo;
  inCarousel: boolean = false;
  @ViewChild('carousel', { static: false }) carousel!: NgbCarousel;
  private offcanvasService = inject(NgbOffcanvas);

  constructor(private route: ActivatedRoute, private pixelperfectService: PixelPerfectService, private sanitizer: DomSanitizer, private modalService: NgbModal) {}

  ngOnInit(): void {
    this.getAlbum();
    this.getAlbumPhotos();
  }

  openCarousel(photo: Photo): void {
    this.inCarousel = true;
    this.carousel.select(photo.id.toString());
    this.carousel.focus();
    this.carousel.pause();
  }

  openDetailsPanel(content: TemplateRef<any>, photo: Photo) {
    this.photo_selected = photo;
		this.offcanvasService.open(content, { position: 'end' });
	}

	closeCarousel(): void {
	  this.offcanvasService.dismiss('Closing Carousel');
	  this.inCarousel = false;
	}

	openPhotoUploadModal(): void {
    const modal = this.modalService.open(ModalPhotoUploadComponent, {});
    modal.result.then(
      (result) => {this.uploadPhotos(result.target.files)},
      (reason) => {},
    );
  }

  openPhotoDeleteModal(photo: Photo): void {
    const modal = this.modalService.open(ModalDeleteConfirmationComponent, {});
    modal.componentInstance.modal_title = photo.name;
    modal.result.then(
      (result) => {this.deletePhoto(photo)},
      (reason) => {},
    );
  }

  getAlbum(): void {
    const album_id = Number(this.route.snapshot.paramMap.get('id'));
    this.pixelperfectService.getAlbum(album_id).subscribe((album) => (this.album = album));
  }

  getAlbumPhotos(): void {
    const album_id = Number(this.route.snapshot.paramMap.get('id'));
    this.pixelperfectService.getAlbumPhotos(album_id).subscribe((photo_list) => {
      this.photo_list = photo_list;
      for (let photo of this.photo_list) {
        this.getPhotoImageThumbnail(photo);
      }
      for (let photo of this.photo_list) {
        this.getPhotoImage(photo);
      }
    });
  }

  uploadPhotos(file_list: FileList): void {
    const album_id = Number(this.route.snapshot.paramMap.get('id'));
    Array.from(file_list).forEach((file) => {
      this.pixelperfectService.addAlbumPhoto(album_id, file).subscribe();
    });
  }

  getPhotoImage(photo: Photo): void {
    this.pixelperfectService.getPhotoImage(photo.id).subscribe((photo_image) => {
      let photo_image_url = URL.createObjectURL(photo_image);
      this.photo_image_list[photo.id] = this.sanitizer.bypassSecurityTrustUrl(photo_image_url);
    })
  }

  getPhotoImageThumbnail(photo: Photo): void {
    this.pixelperfectService.getPhotoImageThumbnail(photo.id).subscribe((photo_image) => {
      let photo_image_url = URL.createObjectURL(photo_image);
      this.photo_image_thumbnail_list[photo.id] = this.sanitizer.bypassSecurityTrustUrl(photo_image_url);
    })
  }

  getValueFromExifData(exif_data_string: string, key: string): string {
    let exif_data = JSON.parse(exif_data_string);
    return exif_data[key];
  }

  convertExposureTime(exposure_time_string: string): string {
    let exposure_time = 1 / parseFloat(exposure_time_string);
    return "1/" + exposure_time + " sec";
  }

  setAlbumCover(photo: Photo) {
    const album_id = Number(this.route.snapshot.paramMap.get('id'));
    this.pixelperfectService.updateAlbumCover(album_id, photo.id).subscribe();
  }

  deletePhoto(photo: Photo) {
    this.pixelperfectService.deletePhoto(photo.id).subscribe((photo) => this.getAlbumPhotos());
  }

  isAdminUser(): boolean {
    return this.pixelperfectService.isAdminUser();
  }
}
