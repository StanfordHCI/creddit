import { Component, OnInit } from '@angular/core';
import { GroupService } from '../shared/services/group.service';
import { Router, Data, ActivatedRoute} from '@angular/router';
import { ToastrService } from 'ngx-toastr';


@Component({
  templateUrl: './admin-group.details.component.html',
  styleUrls: ['./admin-group.component.scss']
})
export class GroupDetailsAdminComponent implements OnInit {
  private isSaved: boolean = false;
  private token: string = '';
  private dataLoaded: boolean= false;
  private groupData: any = '';
  private messageToShow = '';
  constructor(
    private groupService: GroupService,
    private router:Router,
    private route: ActivatedRoute,
    private toastr: ToastrService
  ) {}

  getInitials(name) {
    if(name) {
      let initials = name.match(/\b\w/g) || [];
      initials = ((initials.shift() || '') + (initials.pop() || '')).toUpperCase();
      return initials;
    }
    return '';
  }

  ngOnInit() {
    console.log('Hello Details Group');
    this.route.data.subscribe(
      (data: Data) => {
        this.isSaved = data['isSaved'];
        console.log(data)
      }
    );
    this.messageToShow = 'Typical credit assignment is centralized: it relies on a ' +
      'single supervisor or a small number of peers on the team to ' +
      'make an assessment. For example, a lead researcher ' +
      'often determines author order for all collaborators on a paper, and at ' +
      'a company your supervisors determines your performance review.';


    this.token = this.route.snapshot.params['token'];
    this.groupService.getGroupDetails(this.token)
    .subscribe(data => {
      this.groupData = data;
      this.dataLoaded = false;
    }, err => {
      this.dataLoaded = false;
      this.toastr.error(err, 'Error');
      this.router.navigate(['/']);
      console.log(err)
    })
  }

}
