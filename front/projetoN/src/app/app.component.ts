import { Component } from '@angular/core';
import { NoticiasServiceService } from './noticias-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [NoticiasServiceService],
})
export class AppComponent {
  constructor(private noticiasService: NoticiasServiceService) {}
  title = 'projetoN';
  column_number = 4;
  bypass = false;

  list_of_news_list:any[] = []; 
  list_of_search_terms:string[] = [];

  search1: string = '';
  search2: string = '';
  search3: string = '';
  search4: string = '';
  search5: string = '';
  search6: string = '';
  search7: string = '';
  search8: string = '';
  search9: string = '';
  search10: string = '';

  mock_name1: string = 'Sauro da Silva Suzano';
  mock_name2 = 'Chico Buate';
  mock_name3 = 'Xandico Tronto Toto Kaka Nei'
  

  news_list1:any = [];
  news_list2:any = [];
  news_list3:any = [];
  news_list4:any = [];
  news_list5:any = [];
  news_list6:any = [];
  news_list7:any = [];
  news_list8:any = [];
  news_list9:any = [];
  news_list10:any = [];

  ngOnInit(): void {
    this.list_of_news_list.push(this.news_list1);
    this.list_of_news_list.push(this.news_list2);
    this.list_of_news_list.push(this.news_list3);
    this.list_of_news_list.push(this.news_list4);
    this.list_of_news_list.push(this.news_list5);
    this.list_of_news_list.push(this.news_list6);
    this.list_of_news_list.push(this.news_list7);
    this.list_of_news_list.push(this.news_list8);
    this.list_of_news_list.push(this.news_list9);
    this.list_of_news_list.push(this.news_list10);
    this.list_of_search_terms.push(this.search1);
    this.list_of_search_terms.push(this.search2);
    this.list_of_search_terms.push(this.search3);
    this.list_of_search_terms.push(this.search4);
    this.list_of_search_terms.push(this.search5);
    this.list_of_search_terms.push(this.search6);
    this.list_of_search_terms.push(this.search7);
    this.list_of_search_terms.push(this.search8);
    this.list_of_search_terms.push(this.search9);
    this.list_of_search_terms.push(this.search10);
  }


  
  public transformDateFormat(inputDate:any) {
    const date = new Date(inputDate);
  
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-based
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
  
    const formattedDate = `${day}/${month}/${year} ${hours}:${minutes}`;
  
    return formattedDate;
  }

  public updateColumnsNumber(data: number) {
    this.column_number = data;
    console.log('logging from parente: ', data);
  }
  public updateBypass(data: boolean) {
    this.bypass = data;
    console.log('from parent:',this.bypass);
  }
  public getRange(n: number): number[] {
    return Array.from({ length: n }, (_, index) => index);
  }

  public getGridTemplateColumns(): string {
    return `repeat(${this.column_number}, 350px)`;
  }

  public checkEnterKey(event: any, index:any): void {
    if(event.key == 'Enter') {
      this.fetchNewsV2(this.list_of_search_terms[index], index);
    }
  }

  public fetchNewsV2(term:string, index:any) {
    if(term == '') return;
    if(this.list_of_news_list[index].length > 0) this.list_of_news_list[index].length = 0;
    this.noticiasService.fetchNews(term).subscribe(
      (data) => {
        for(let item of data) {
          switch (item.fonte) {
            case 'Poder360':
              item.thumb = "https://static.poder360.com.br/2022/04/logo-poder360-1-1-280x280.png";
              break;
            case 'Folha de S. Paulo':
              item.thumb = "https://yt3.googleusercontent.com/N2fcR7REBeaSDM5eVvOJNDZRfn5vwPMSqnYGzBXnVbA9XNeduuQvbJrn745SGmFM9KF4FSSzJTA=s176-c-k-c0x00ffffff-no-rj"
              break;
            case 'Metropoles':
              item.thumb = "https://yt3.googleusercontent.com/ytc/AIf8zZT9OcRPYvtD7LiHdHVteyqbP4zzdrfcCJov-ORCiG8=s176-c-k-c0x00ffffff-no-rj";
              item.fonte = 'Metrópoles'
              break;
            case 'Gazeta':
              item.thumb = "https://media.gazetadopovo.com.br/2019/12/17112031/meta-image-gazeta-do-povo-new.png";
              item.fonte = 'Gazeta do Povo'
              break;
            case 'Correio Braziliense':
              item.thumb = "https://play-lh.googleusercontent.com/MmOuY7R_3lKjXbXjpLjjeUupp0CIfaoI2pJDBaB7uvCQsJ3ndQifS7J7n43K7ZuZ9A";
              break;
            case 'diario do poder':
              item.thumb = "https://uploads.diariodopoder.com.br/2022/08/18426125-cch_twitter.jpg"
              item.fonte = 'Diário do Poder'
              break;
            default:
              item.thumb = "https://i.kym-cdn.com/entries/icons/original/000/045/146/son-goku-thumb-up.png"
          }
          if(item.titulo.length > 65) {
            let new_titulo = '';
            for (let i = 0; i < 65; i++) new_titulo += item.titulo[i]
            new_titulo += '...'
            item.titulo = new_titulo;
          }
          const now = Date.now();
          const tstamp = new Date(item.data).getTime();

          item.data = this.transformDateFormat(item.data);
          const tdif = now - tstamp; // milisecs
          if(tdif < (1000 * 60 * 60 * 24)) { // menos que um dia atrás
            if(tdif < 1000 * 60 * 60) { // menos de uma hora atrás
              const minutes = Math.floor(tdif / (1000 * 60));
              item.tdif_display = `(${minutes} minutos)`;
            }
            else { // mais de uma hora
              const horas = Math.floor(tdif / (1000 * 60 * 60)); // pega parte inteira da divisao arredondando p baixo
              item.tdif_display = `(${horas} horas)`
            }
          } 
          else { // mais que um dia atrás
            const dias = Math.floor(tdif / (1000 * 60 * 60 * 24));
            item.tdif_display = `(${dias} dias)`
          }
          
          this.list_of_news_list[index].push(item)
        }
        setTimeout(() => {
          console.log(`rechamando fetchnewsv2 com os args: ${this.list_of_search_terms[index]} e ${index}`)
          this.fetchNewsV2(this.list_of_search_terms[index],index);
        },60000 * 5);
        console.log(data); // Handle the data here
      },
      (error) => {
        console.error('Error fetching data:', error);
      });
  }


}
