import { NgModule, ApplicationRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { CreateGroupComponent } from './create-group/create-group.component';
import { GroupDetailsAdminComponent } from './admin-group/admin-group.details.component';
import { GroupEditAdminComponent } from './admin-group/admin-group.edit.component';
import { ScoreEditComponent } from './score/score.component.edit';
import { ScoreDetailComponent } from './score/score.component.detail';
import { ApiService } from './shared';
import { GroupService } from './shared/services/group.service';
import { routing } from './app.routing';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ModalModule } from 'ngx-bootstrap';
import { LaddaModule } from 'angular2-ladda';
import { ToastrModule } from 'ngx-toastr';


import { removeNgStyles, createNewHosts } from '@angularclass/hmr';

@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpModule,
    FormsModule,
    routing,
    NgbModule.forRoot(),
    ModalModule.forRoot(),
    LaddaModule.forRoot({
      style: 'slide-left'
    }),
    ToastrModule.forRoot()
  ],
  declarations: [
    AppComponent,
    HomeComponent,
    AboutComponent,
    CreateGroupComponent,
    GroupDetailsAdminComponent,
    GroupEditAdminComponent,
    ScoreEditComponent,
    ScoreDetailComponent
  ],
  providers: [
    ApiService,
    GroupService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(public appRef: ApplicationRef) {}
  hmrOnInit(store) {
    console.log('HMR store', store);
  }
  hmrOnDestroy(store) {
    let cmpLocation = this.appRef.components.map(cmp => cmp.location.nativeElement);
    // recreate elements
    store.disposeOldHosts = createNewHosts(cmpLocation);
    // remove styles
    removeNgStyles();
  }
  hmrAfterDestroy(store) {
    // display new elements
    store.disposeOldHosts();
    delete store.disposeOldHosts;
  }
}
