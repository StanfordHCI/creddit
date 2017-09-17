import { Component, OnInit } from '@angular/core';
import { GroupService } from '../shared/services/group.service';
import { ToastrService } from 'ngx-toastr';
import { Router, ActivatedRoute} from '@angular/router';
import { AppSettings } from '../app.constant';


@Component({
  templateUrl: './score.component.edit.html',
  styleUrls: ['./score.component.scss']
})
export class ScoreEditComponent implements OnInit {
  private groupData: any = [];
  private token: string = '';
  private totalCount: number;
  isLoading = false;
  private formValid: boolean;
  private pointsDistributed: number;
  private remainingPoints: number;
  constructor(
    private groupService: GroupService,
    private router: Router,
    private toastr: ToastrService,
    private route: ActivatedRoute
  ) {
    this.pointsDistributed = 0;
    this.formValid = true;
    this.remainingPoints = 100;
  }


  getInitials(name) {
    if (name) {
      let initials = name.match(/\b\w/g) || [];
      initials = ((initials.shift() || '') + (initials.pop() || '')).toUpperCase();
      return initials;
    }
    return '';
  }


  processScoresCount() {
    this.pointsDistributed = 0;
    for(let user of this.groupData.from_credit_user) {
      user.score = parseInt(user.score) || 0;
      let score = user.score;
      this.pointsDistributed += score;
    }
    this.remainingPoints = Math.abs(this.totalCount - this.pointsDistributed);
    if(this.pointsDistributed > 100) {
      this.formValid = false;
    } else {
      this.formValid = true;
    }
    console.log(this.pointsDistributed);
  }


  changeScoreValue() {
    console.log(this.groupData)
    this.processScoresCount();
  }

  addpoints(creditScore) {
    if(this.pointsDistributed < 100) {
      creditScore.score = creditScore.score + 1;
      this.processScoresCount();
    }
  }

  subpoints(creditScore) {
    if(creditScore.score > 0)
    {
      creditScore.score = creditScore.score - 1;
      this.processScoresCount();
    }
  }

  postScore() {
    this.isLoading = true;
    this.groupService.postGroupDetailsForScore(this.token, this.groupData)
      .subscribe(
        data => {
          console.log(data);
          this.isLoading = false;
          this.router.navigate(['/scores', this.token, 'success']);
        },
        err => {
          this.isLoading = false;
          this.toastr.error(err, 'Error');
          console.log(err);
        }
      );
  }
  ngOnInit() {
    this.totalCount = AppSettings.TOTAL_POINTS;
    this.token = this.route.snapshot.params['token'];
    this.groupService.getGroupDetailsForScore(this.token)
      .subscribe(data => {
        this.groupData = data;
        for(let user of data.from_credit_user) {
          let score = parseInt(user.score);
          this.pointsDistributed += score;
        }
      }, err => {
        this.router.navigate(['/']);
        console.log(err)
      })
  }
}
