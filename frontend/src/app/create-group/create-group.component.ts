import { Component, OnInit } from '@angular/core';
import { GroupService } from '../shared/services/group.service';
import { UserModel } from '../shared/models/user-model';
import { Router} from '@angular/router';
import { TemplateRef } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/modal-options.class';


@Component({
  templateUrl: './create-group.component.html',
  styleUrls: ['./create-group.component.scss']
})
export class CreateGroupComponent implements OnInit {
  public modalRef: BsModalRef;
  // userObject: UserModel = new UserModel();
  groupData = {
    name : '',
    credit_admin : [
      new UserModel()
    ],
    credit_users : [
      new UserModel()
    ]

  };
  constructor(
    private groupService: GroupService,
    private router:Router,
    private modalService: BsModalService
  ) {
  }

  public openModal(template: TemplateRef<any>) {
    this.modalRef = this.modalService.show(template);
  }

  addMoreUser() {
    this.groupData.credit_users.push(new UserModel());
  }

  removeUser(index) {
    this.groupData.credit_users.splice(index, 1);
  }

  createGroup(sendToAll: boolean) {
    console.log(sendToAll);
    this.groupService.createGroup(this.groupData)
      .subscribe(
        data => {
          console.log(data)
          this.modalRef.hide();
          this.router.navigate(['/']);
        },
        err => {
          console.log(err)
        }
      );
  }
  ngOnInit() {
    console.log('Hello Create Group');
  }



}
