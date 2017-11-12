import { Component, OnInit } from '@angular/core';
import { GroupService } from '../shared/services/group.service';
import { ToastrService } from 'ngx-toastr';
import { Router, ActivatedRoute} from '@angular/router';

@Component({
  templateUrl: './score.component.detail.html',
  styleUrls: ['./score.component.scss']
})
export class ScoreDetailComponent implements OnInit {
  private groupData = [];
  private token: string = '';
  // trigger-variable for Ladda
  isLoading = false;
  private pathToCopy: string;
  isDecline = false;
  sub: any;
  constructor(
    private groupService: GroupService,
    private router: Router,
    private toastr: ToastrService,
    private route: ActivatedRoute
  ) {
    let pathToCo = window.location.href;
    this.pathToCopy = pathToCo.substring(0, pathToCo.lastIndexOf("/success"))
  }

  getInitials(name) {
    if (name) {
      let initials = name.match(/\b\w/g) || [];
      initials = ((initials.shift() || '') + (initials.pop() || '')).toUpperCase();
      return initials;
    }
    return '';
  }


  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  ngOnInit() {
    this.token = this.route.snapshot.params['token'];
    this.sub = this.route.queryParams.subscribe(params => {
       this.isDecline = params['dec'] || false;
       console.log(this.isDecline)
    });
    this.groupService.getGroupDetailsForScore(this.token)
      .subscribe(data => {
        this.groupData = data;
        console.log(this.groupData)
      }, err => {
        this.toastr.error(err, 'Error');
        this.router.navigate(['/']);
        console.log(err)
      })
  }
}
