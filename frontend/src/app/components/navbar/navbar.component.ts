import { Component, HostListener, Inject, Output, EventEmitter } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { RouterLink } from '@angular/router';
import { PixelPerfectService } from '../../services/pixelperfect.service';

@Component({
    selector: 'app-navbar',
    imports: [RouterLink],
    templateUrl: './navbar.component.html',
    styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  documentElement: any;
  inFullscreen: boolean = false;
  @Output() openAddDialogEvent = new EventEmitter();

  constructor(@Inject(DOCUMENT) private document: any, private pixelperfectService: PixelPerfectService) {}

  ngOnInit(): void {
    this.documentElement = document.documentElement;
    this.setStateFullscreen();
    this.pixelperfectService.getUserCurrent().subscribe();
  }

  @HostListener('document:fullscreenchange', ['$event'])
  @HostListener('document:webkitfullscreenchange', ['$event'])
  @HostListener('document:mozfullscreenchange', ['$event'])
  @HostListener('document:MSFullscreenChange', ['$event'])
  stateChangeFullscreen(event: any): void {
    this.setStateFullscreen();
  }

  setStateFullscreen(): void {
    if (document.fullscreenElement) {
      this.inFullscreen = true;
    } else {
      this.inFullscreen = false;
    }
  }

  toggleFullscreen(): void {
    if (!this.inFullscreen) {
      this.openFullscreen();
    }
    else {
      this.closeFullscreen();
    }
  }

  openFullscreen(): void {
    if (this.documentElement.requestFullscreen) {
      this.documentElement.requestFullscreen();
    } else if (this.documentElement.mozRequestFullScreen) {
      /* Firefox */
      this.documentElement.mozRequestFullScreen();
    } else if (this.documentElement.webkitRequestFullscreen) {
      /* Chrome, Safari and Opera */
      this.documentElement.webkitRequestFullscreen();
    } else if (this.documentElement.msRequestFullscreen) {
      /* IE/Edge */
      this.documentElement.msRequestFullscreen();
    }
  }

  closeFullscreen(): void {
    if (this.document.exitFullscreen) {
      this.document.exitFullscreen();
    } else if (this.document.mozCancelFullScreen) {
      /* Firefox */
      this.document.mozCancelFullScreen();
    } else if (this.document.webkitExitFullscreen) {
      /* Chrome, Safari and Opera */
      this.document.webkitExitFullscreen();
    } else if (this.document.msExitFullscreen) {
      /* IE/Edge */
      this.document.msExitFullscreen();
    }
  }

  supportFullscreen(): boolean {
    return typeof this.documentElement.requestFullscreen !== 'undefined' ||
      typeof this.documentElement.mozRequestFullScreen !== 'undefined' ||
      typeof this.documentElement.webkitRequestFullscreen !== 'undefined' ||
      typeof this.documentElement.msRequestFullscreen !== 'undefined' ||
      typeof this.document.exitFullscreen !== 'undefined' ||
      typeof this.document.mozCancelFullScreen !== 'undefined' ||
      typeof this.document.webkitExitFullscreen !== 'undefined';
  };

  openAddDialog(): void {
    this.openAddDialogEvent.emit();
  }

  isAdminUser(): boolean {
    return this.pixelperfectService.isAdminUser();
  }

  logout(): void {
    this.pixelperfectService.logout().subscribe();
  }
}
