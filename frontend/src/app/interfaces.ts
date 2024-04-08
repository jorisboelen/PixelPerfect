export interface Album {
  id: number;
  name: string;
  date_created: Date;
  cover_photo: Photo | undefined;
}

export interface Photo {
  id: number;
  album_id: number;
  name: string;
  date_created: Date;
  date_taken: Date;
  file_name: string;
  format: string;
  mode: string;
  width: number;
  height: number;
  exif_data: string;
}

export interface User {
  username: string;
  is_admin: boolean;
}

export enum NotificationLevel {
  ERROR = 'danger',
  WARN = 'warning',
  INFO = 'success',
  DEBUG = 'info',
}

export interface NotificationMessage {
  level: NotificationLevel;
  message: string;
  timestamp: Date;
}
