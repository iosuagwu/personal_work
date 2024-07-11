import { Component, OnInit, NgZone } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { UserdataService } from '../../userdata.service';
import { AuthService, FacebookLoginProvider, SocialUser } from 'angularx-social-login';
import { Router } from '@angular/router';

@Component({
  selector: 'app-primary',
  templateUrl: './primary.component.html',
  styleUrls: ['./primary.component.css']
})
export class PrimaryComponent implements OnInit {

  public email = "";
  public password = "";
  public user: SocialUser;
  public loggedIn: boolean;
  public userInfo: any = [];
  //Facebook API sign in stuff
  constructor(
    private authService: AuthService,
    private userdataService: UserdataService,
    private ngZone: NgZone,
    private router: Router
  ) { }

  signInWithFB(): void {
    this.authService.signIn(FacebookLoginProvider.PROVIDER_ID);
  }

  signOut(): void {
    this.authService.signOut();
  }
  ngOnInit() {
    this.loadUsers();
    this.authService.authState.subscribe((user) => {
      this.user = user;
      this.loggedIn = (user != null);
      console.log(this.user);
    });
  }
  //Get request stuff
  //constructor(private userdataService: UserdataService) {}

  loadUsers() {
    return this.userdataService.getData().subscribe((data: {}) => {
      this.userInfo = data;
    })
  }

  loginUser() {
   	// body...
    //console.log(event);
    for(var em of this.userInfo) {
      if((this.email == (em.EMail)) && (this.password==(em.Password)))
        this.ngZone.run(() => this.router.navigateByUrl('/profile'));
      else
        console.log("Incorrect Email or Password! Try Again");
    }
    console.log(this.email);

   	if((this.email=="iosuagwu@villanova.edu") && (this.password == "william")){
   		console.log("Welcome!");
   	} else{
   		console.log("Incorrect Email or Password! Try Again");
   	}
   }

}
