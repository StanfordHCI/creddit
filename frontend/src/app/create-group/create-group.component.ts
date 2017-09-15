import { Component, OnInit } from '@angular/core';
import { GroupService } from '../shared/services/group.service';
import { UserModel } from '../shared/models/user-model';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';

@Component({
  templateUrl: './create-group.component.html',
  styleUrls: ['./create-group.component.scss']
})
export class CreateGroupComponent implements OnInit {
  groupData = {
    name : '',
    credit_admin : [
      new UserModel()
    ],
    credit_users : [
      new UserModel()
    ]
  };
  // trigger-variable for Ladda
  isLoading = false;
  constructor(
    private groupService: GroupService,
    private router: Router,
    private toastr: ToastrService
  ) {
  }

  addMoreUser() {
    this.groupData.credit_users.push(new UserModel());
  }

  removeUser(index) {
    if(this.groupData.credit_users.length > 1)
      this.groupData.credit_users.splice(index, 1);
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
          this.toastr.success('Group members should check their emails for the link.', 'Group Created');
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
    console.log('Hello Create Group');
  }



}
