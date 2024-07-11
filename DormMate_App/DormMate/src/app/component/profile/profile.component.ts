import { Component, OnInit, NgZone } from '@angular/core';
import { UserdataService } from '../../userdata.service';
import { AuthService, FacebookLoginProvider, SocialUser } from 'angularx-social-login';
import { Router, ActivatedRoute } from '@angular/router';
import { FormGroup, FormControl, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  usersList: any = [];
  updateUser: FormGroup;

  public user: SocialUser;
  public loggedIn: boolean;

  constructor(private authService: AuthService,
    private userdataService: UserdataService,
    public fb: FormBuilder,
    private ngZone: NgZone,
    private router: Router,
    private actRoute: ActivatedRoute,
  ) {
    var id = this.actRoute.snapshot.paramMap.get('id');
    this.userdataService.getUser(1).subscribe((data) => {
      this.usersList = data;
    });
   }



  signInWithFB(): void {
    this.authService.signIn(FacebookLoginProvider.PROVIDER_ID);
  }

  signOut(): void {
    this.authService.signOut();
  }
  ngOnInit() {
    this.authService.authState.subscribe((user) => {
      this.user = user;
      this.loggedIn = (user != null);
      console.log(this.user);
    });
  }

}
