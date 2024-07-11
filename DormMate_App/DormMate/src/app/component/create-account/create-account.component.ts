import { Component, OnInit, NgZone } from '@angular/core';
import { FormGroup, FormControl, FormBuilder } from '@angular/forms';
import { UserdataService } from '../../userdata.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-account',
  templateUrl: './create-account.component.html',
  styleUrls: ['./create-account.component.css']
})
export class CreateAccountComponent implements OnInit {

  public email = "";
  public password1= "";
  public password2= "";
  public change = {
    email: "afreay@villanova.edu",
    password: "test123"
  };
  userForm: FormGroup;
  userArr: any = [];

  constructor(
    private userdataService: UserdataService,
    public fb: FormBuilder,
    private ngZone: NgZone,
    private router: Router
  ) {}

  ngOnInit() {
    this.addUser();
  }

  addUser() {
    this.userForm = this.fb.group({
      EMail: [''],
      Password: [''],
      VUID: ['']
    })
  }

  //public userdata = JSON.stringify(this.change);
  register(){
    this.userdataService.newUser(this.userForm.value).subscribe(res => {
      console.log('Account Created')
      this.ngZone.run(() => this.router.navigateByUrl('/editProfile'))
    });
    //this.userdataService.newUser(this.userdata).subscribe((response) => {console.log(response)});
  }

  checkCredentials(){
  	if(this.password1 == this.password2){
  		console.log("Account Creation Successfull");
  	} else{
      console.log("Passwords do not match");
    }
  }

}
