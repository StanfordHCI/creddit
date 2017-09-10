import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

import '../style/app.scss';

@Component({
  selector: 'my-app', // <my-app></my-app>
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  url = 'https://github.com/preboot/angular2-webpack';
  title: string;

  constructor(private router: Router) {
  }
  ngOnInit() {
    this.router.events.subscribe((evt) => {
      if (!(evt instanceof NavigationEnd)) {
        return;
      }
      // window.scrollTo(0, 0)
      var scrollStep = -window.scrollY / (500 / 15),
      scrollInterval = setInterval(function(){
        if ( window.scrollY != 0 ) {
          window.scrollBy( 0, scrollStep );
        }
        else clearInterval(scrollInterval);
      },15);
    });
  }
}
