import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { PixelPerfectService } from '../../services/pixelperfect.service';
import { UserLoginModel } from '../../models';

@Component({
    selector: 'app-login',
    imports: [FormsModule],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {
  user_login: UserLoginModel = new UserLoginModel();

  constructor(private pixelperfectService: PixelPerfectService) {}

  login(): void {
    this.pixelperfectService.login(this.user_login).subscribe();
  }
}
