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
  private groupData = [];
  private token: string = '';
  private totalCount: number;
  // trigger-variable for Ladda
  isLoading = false;
  constructor(
    private groupService: GroupService,
    private router: Router,
    private toastr: ToastrService,
    private route: ActivatedRoute
  ) {
  }


  getInitials(name) {
    if (name) {
      let initials = name.match(/\b\w/g) || [];
      initials = ((initials.shift() || '') + (initials.pop() || '')).toUpperCase();
      return initials;
    }
    return '';
  }

  addpoints(creditScore) {
    creditScore.score = creditScore.score + 1;
  }

  subpoints(creditScore) {
    creditScore.score = creditScore.score - 1;
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
        console.log(this.groupData)
      }, err => {
        this.router.navigate(['/']);
        console.log(err)
      })
  }
}
