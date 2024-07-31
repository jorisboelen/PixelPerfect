import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import {} from '@angular/common/http';
import { provideRouter, withHashLocation } from '@angular/router';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes, withHashLocation()), importProvidersFrom(HttpClientModule)]
};
