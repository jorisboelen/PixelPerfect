/** https://github.com/ShankyTiwari/ng-navigator-share */
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ShareService {
  webNavigator: any = null;

  constructor() {
    this.webNavigator = window.navigator;
  }

  canShare(): boolean {
    return this.webNavigator !== null && this.webNavigator.share !== undefined;
  }

  canShareFile(file: []): boolean {
    return this.webNavigator !== null && this.webNavigator.share !== undefined && this.webNavigator.canShare({ files: file });
  }

  share({ title, text, url, files }: { title?: string, text?: string, url?: string, files?: any[] }) {
    return new Promise(async (resolve, reject) => {
      if (this.webNavigator !== null && this.webNavigator.share !== undefined) {
          try {
            const shareObject: ShareObject = {
                title,
                text,
                url
            };
            if (files && files.length !== 0) {
                shareObject.files = files;
            }
            const isShared = await this.webNavigator.share(shareObject);
            resolve({
              shared: true
            });
          } catch (error) {
            reject({
              shared: false,
              error
            });
          }
      } else {
        reject({
          shared: false,
          error: `This service/api is not supported in your Browser`
        });
      }
    });
  }
}

interface ShareObject {
  title?: string;
  text?: string;
  url?: string;
  files?: any[];
}
