import { Component, OnInit } from '@angular/core';
import { GroupService } from '../shared/services/group.service';

@Component({
  selector: 'my-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  private groupCount: number;
  constructor(private groupService: GroupService) {
    // Do stuff
    this.groupCount = 0;
  }

  ngOnInit() {
    this.groupService.getGroupCount()
      .subscribe(data => {
        for(let i = 0; i <= data.number_of_groups; i++) {
          this.groupCount++;
        }
      });
    console.log('Hello Home');
  }

}
