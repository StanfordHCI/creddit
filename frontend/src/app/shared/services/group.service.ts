import { Injectable } from '@angular/core';
import {Http, Response} from '@angular/http';
import {Observable} from 'rxjs/Observable';
import {AppSettings} from '../../app.constant';

@Injectable()
export class GroupService {
  private apiUrl: string = AppSettings.API_ENDPOINT;

  constructor(private http: Http){}

  /**
   * Create the Group & its users
   */
  createGroup(data: any): Observable<string> {
    return this.http.post(`${this.apiUrl}/app/api/groups/CreditGroupCreateApi/`, data)
      .map(res => res.json())
      .catch(this.handleError);
  }


  /**
   * Handle any errors from the API
   */
  private handleError(err) {
    let errMessage: string;

    if (err instanceof Response) {
      let body   = err.json() || '';
      let error  = body.error || JSON.stringify(body);
      errMessage = `${err.statusText || ''} ${error}`;
    } else {
      errMessage = err.message ? err.message : err.toString();
    }

    return Observable.throw(errMessage);
  }

}
