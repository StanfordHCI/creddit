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
  private pathToCopy: string;
  private countSubmissions: number;

  intervalId;

  single: any[];

  view: any[] = [700, 400];
  // options
  showLegend = true;

  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };

  // pie
  showLabels = true;
  explodeSlices = false;
  doughnut = false;

  constructor(
    private groupService: GroupService,
    private router:Router,
    private route: ActivatedRoute,
    private toastr: ToastrService
  ) {
    this.pathToCopy = window.location.href;
    this.countSubmissions = 0;
    this.single = [];
  }

  getInitials(name) {
    if(name) {
      let initials = name.match(/\b\w/g) || [];
      initials = ((initials.shift() || '') + (initials.pop() || '')).toUpperCase();
      return initials;
    }
    return '';
  }

  copyTextCallback(eventData) {
    this.toastr.success('Private url has been copied to your clipboard.', 'Copied');
    console.log(eventData)
  }

  ngOnInit() {
    console.log('Hello Details Group');
    this.route.data.subscribe(
      (data: Data) => {
        this.isSaved = data['isSaved'];
        console.log(data)
      }
    );



    this.token = this.route.snapshot.params['token'];
    this.groupService.getGroupDetails(this.token)
    .subscribe(data => {
      this.groupData = data;
      if(this.groupData.credit_users) {
        var graphArray = [];
        for (let user of this.groupData.credit_users) {
          let graphObj = {
            "name" : user.name,
            "value" : user.score
          };
          graphArray.push(graphObj);
          if(user.is_submitted != false) {
            this.countSubmissions++;
          }
        }
        this.single = [...graphArray];
        console.log(this.single)
        var submissionPlaceholder = 'No';
        if(this.countSubmissions != 0)
        {
          submissionPlaceholder = (this.countSubmissions).toString();
        }
        this.messageToShow = submissionPlaceholder + ' group members have entered their credit scores ' +
          'yet. Tell your group members to check their email for a link to enter their ' +
          'scores. This is a good time to open the email we sent you and use it to enter your scores! ' +
          'You have also received an email that lets you see the results and add or remove group members.';
      }
      console.log(this.groupData)
      this.dataLoaded = false;
    }, err => {
      this.dataLoaded = false;
      this.toastr.error(err, 'Error');
      this.router.navigate(['/']);
      console.log(err)
    })
  }

}
