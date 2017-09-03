import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { CreateGroupComponent } from './create-group/create-group.component';
import { GroupDetailsAdminComponent } from './admin-group/admin-group.details.component';
import { GroupEditAdminComponent } from './admin-group/admin-group.edit.component';
import { ScoreEditComponent } from './score/score.component.edit';
import { ScoreDetailComponent } from './score/score.component.detail';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'groups', component: CreateGroupComponent },
  {
    path: 'manage-group/:token',
    component: GroupDetailsAdminComponent,
    data : {
      isSaved: false
    }
  }, {
    path: 'edit-group/:token',
    component: GroupEditAdminComponent
  }, {
    path: 'scores/:token',
    component: ScoreEditComponent
  }, {
    path: 'scores/:token/success',
    component: ScoreDetailComponent
  },
  { path: 'about', component: AboutComponent }
];

export const routing = RouterModule.forRoot(routes);
