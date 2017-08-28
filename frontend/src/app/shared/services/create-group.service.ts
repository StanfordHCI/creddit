import { Injectable } from '@angular/core';
import {Http, Response} from '@angular/http';
import {Observable} from 'rxjs/Observable';
import {AppSettings} from '../../app.constant';

@Injectable()
export class CreateGroupService {
  private apiUrl: string = AppSettings.API_ENDPOINT;
  private loggedIn: boolean = false;
  private loggedInData: any = {};

  constructor(private http: Http){
    this.loggedIn = !!localStorage.getItem('api_auth_token');
    if(this.loggedIn)
        this.loggedInData = JSON.parse(localStorage.getItem('api_user_data'));
  }

  /**
   * Check if the user is logged in
   */
  isLoggedIn() {
    return this.loggedIn;
  }


/**
   * Check if the user is logged in
   */
  getLoggedInData() {
    return this.loggedInData;
  }



  /**
   * Log the user in
   */
  login(username: string, password: string): Observable<string> {
    return this.http.post(`${this.apiUrl}/auth/api/Login/`, { username, password })
      .map(res => res.json())
      .do(res => {
        if (res.token)
        {
          this.loggedIn = true;
            localStorage.setItem('api_auth_token', res.token);
            localStorage.setItem('api_user_data', JSON.stringify(res));
        }
      })
      .catch(this.handleError);
  }


    /**
   * Log the user in
   */
  register(username: string, password: string, last_name: string, first_name: string): Observable<string> {
    let userData = {
        username : username,
        email : username,
        password : password,
        first_name : first_name,
        last_name : last_name
    };
    return this.http.post(`${this.apiUrl}/auth/api/SignUp/`, userData)
      .map(res => res.json())
      .do(res => {
        if (res.token)
        {
          this.loggedIn = true;
            localStorage.setItem('api_auth_token', res.token);
            localStorage.setItem('api_user_data', JSON.stringify(res));
        }
      })
      .catch(this.handleError);
  }

    /**
   * Log the user out
   */
  logout() {
    localStorage.removeItem('api_auth_token');
    localStorage.removeItem('api_user_data');
    this.loggedIn = false;
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

      /**
   * Log the user in
   */
  subscribeEmail(email: string): Observable<string> {
    let userData = {
        email : email
    };
    return this.http.post(`${this.apiUrl}/redshift/api/UserEmailList/`, userData)
      .map(res => res.json())
      .do(res => {
        console.log(res)
      })
      .catch(this.handleError);
  }

}
