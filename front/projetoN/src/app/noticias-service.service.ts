import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class NoticiasServiceService {

  constructor(private httpClient: HttpClient) { }

  public fetchNews(term: string) {
     // Make a GET request to your Express server
     return this.httpClient.get<any[]>(`http://177.71.192.95:3000/v1/search/${term}`);
  }
}
