import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';
import { UserData } from './UserData';

//const localUrl = "http://127.0.0.1:8080/v0/newAccount";
const localUrl = "http://localhost:3000/Users";
@Injectable({
  providedIn: 'root'
})
export class UserdataService {

  constructor(private http : HttpClient) { }

  // Http Headers
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  }

  //POST
  newUser(data): Observable<UserData>{
    return this.http.post<UserData>(localUrl, JSON.stringify(data), this.httpOptions)
    .pipe(
      map(data=> data),
      retry(1),
      catchError(this.errorHandl)
    );
  }

  // GET
  getData(): Observable<UserData> {
    return this.http.get<UserData>(localUrl)
    .pipe(
      retry(1),
      catchError(this.errorHandl)
    )
  }

  // GET specific user
  getUser(id): Observable<UserData> {
    return this.http.get<UserData>(localUrl + "/" + id)
    .pipe(
      retry(1),
      catchError(this.errorHandl)
    )
  }

  // PUT
  UpdateUser(id, data): Observable<UserData> {
    return this.http.put<UserData>(localUrl + "/" + id, JSON.stringify(data), this.httpOptions)
    .pipe(
      retry(1),
      catchError(this.errorHandl)
    )
  }

  // DELETE
  DeleteUser(id){
    return this.http.delete<UserData>(localUrl + id, this.httpOptions)
    .pipe(
      retry(1),
      catchError(this.errorHandl)
    )
  }

  // Error handling
  errorHandl(error) {
     let errorMessage = '';
     if(error.error instanceof ErrorEvent) {
       // Get client-side error
       errorMessage = error.error.message;
     } else {
       // Get server-side error
       errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
     }
     console.log(errorMessage);
     return throwError(errorMessage);
  }

}
