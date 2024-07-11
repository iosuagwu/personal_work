import { Component, OnInit, NgZone } from '@angular/core';
import { FormGroup, FormControl, FormBuilder } from '@angular/forms';
import { UserdataService } from '../../userdata.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-match',
  templateUrl: './match.component.html',
  styleUrls: ['./match.component.css']
})
export class MatchComponent implements OnInit {

  usersList: any = [];
  num: number = 2;
  match: boolean = false;
  images: string[] = [
    "https://villanova.com/images/2019/10/2/9_27_19_186.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_221.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_194.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_188.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_195.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_200.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_220.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_203.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_212.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_214.jpg?width=300",
    "https://villanova.com/images/2018/10/4/Becky_Ducar.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_223.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_217.jpg?width=300",
    "https://villanova.com/images/2019/10/2/9_27_19_206.jpg?width=300"
  ];
  imgURL: string = "";

  constructor(
    private actRoute: ActivatedRoute,
    private userdataService: UserdataService,
    public fb: FormBuilder,
    private ngZone: NgZone,
    private router: Router
  ) { }

  ngOnInit() {
    this.rollMatches();
  }

  rollMatches() {
    this.userdataService.getUser(this.num).subscribe((data) => {
      this.usersList = data;
    });
    this.imgURL= this.images[this.num-2];
    if(this.num==16){
      this.ngZone.run(() => this.router.navigateByUrl('/messages'))
    }
    this.num++;
    if((this.num ==4) || (this.num == 5) || (this.num == 16)){
      this.match = true;
    }
    else{
      this.match = false;
    }
  }

}
