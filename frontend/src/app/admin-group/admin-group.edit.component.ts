import { Component, OnInit } from '@angular/core';
import { GroupService } from '../shared/services/group.service';
import { Router, Data, ActivatedRoute} from '@angular/router';
import { ToastrService } from 'ngx-toastr';


@Component({
  templateUrl: './admin-group.edit.component.html',
  styleUrls: ['./admin-group.component.scss']
})
export class GroupEditAdminComponent implements OnInit {
  private isSaved: boolean = false;
  private token: string = '';
  private dataLoaded: boolean= false;
  private groupData: any = '';
  private messageToShow = '';
  private isLoading;
  constructor(
    private groupService: GroupService,
    private router:Router,
    private route: ActivatedRoute,
    private toastr: ToastrService
  ) {
    this.isLoading = false;
  }

  getInitials(name) {
    if(name) {
      let initials = name.match(/\b\w/g) || [];
      initials = ((initials.shift() || '') + (initials.pop() || '')).toUpperCase();
      return initials;
    }
    return '';
  }

  trackByFn(i) {
    return i;
  }

  addMoreUser() {
    console.log(this.groupData.credit_users)
    this.groupData.credit_users.push({name: "", email : ""});
    console.log(this.groupData.credit_users)
  }

  sendEmail(userData) {
    if(userData.emailSending)
      return false;
    console.log('dasd');
    userData.emailSending = true;
    this.groupService.sendEmail(userData.id)
      .subscribe(() => {
        this.toastr.success('Email has been shared with the Group Member', 'Email Sent');
        userData.emailSending = false;
      }, err => {
        userData.emailSending = true;
        this.toastr.success(err, 'Error');
      })
  }

  removeUser(index) {
    if(this.groupData.credit_users.length > 2)
      this.groupData.credit_users.splice(index, 1);
    console.log(this.groupData.credit_users)
  }

  ngOnInit() {
    console.log('Hello Details Group');
    this.route.data.subscribe(
      (data: Data) => {
        this.isSaved = data['isSaved'];
        console.log(data)
      }
    );
    this.messageToShow = 'Typical credit assignment is centralized: it relies ' +
      'on a single supervisor or a small number of peers on the ' +
      'team to make an assessment. For example, a lead researcher ' +
      'often determines author order for all collaborators on a ' +
      'paper, and at a company your supervisors determines your performance review.';


    this.token = this.route.snapshot.params['token'];
    this.groupService.getGroupDetails(this.token)
    .subscribe(data => {
      this.groupData = data;
      this.dataLoaded = false;
    }, err => {
      this.dataLoaded = false;
      this.router.navigate(['/']);
      console.log(err)
    })
  }


  editGroup() {
    this.isLoading = true;
    this.groupService.editGroup(this.token, this.groupData)
      .subscribe(
        data => {
          console.log(data);
          this.isLoading = false;
          let token = data.token;
          this.toastr.success('Group members should check their emails for the link.', 'Group Updated');
          this.router.navigate(['/manage-group', token]);
        },
        err => {
          this.isLoading = false;
          this.toastr.error(err, 'Error');
          console.log(err);
        }
      );
  }

}
