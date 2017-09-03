import { Component, OnInit } from '@angular/core';
import { GroupService } from '../shared/services/group.service';
import { ToastrService } from 'ngx-toastr';
import { Router, ActivatedRoute} from '@angular/router';


@Component({
  templateUrl: './score.component.html',
  styleUrls: ['./score.component.scss']
})
export class ScoreComponent implements OnInit {
  private groupData = {};
  private token: string = '';
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

  createGroup() {
    this.isLoading = true;
    this.groupService.createGroup(this.groupData)
      .subscribe(
        data => {
          console.log(data);
          this.isLoading = false;
          let token = data.token;
          this.router.navigate(['/manage-group', token]);
        },
        err => {
          this.isLoading = false;
          this.toastr.error(err, 'Error');
          console.log(err);
        }
      );
  }
  ngOnInit() {
    console.log('Hello Score User');
    this.token = this.route.snapshot.params['token'];
    this.groupService.getGroupDetailsForScore(this.token)
      .subscribe(data => {
        this.groupData = data;
      }, err => {
        this.router.navigate(['/']);
        console.log(err)
      })
  }



}
