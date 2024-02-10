import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'namePipe'
})
export class NamePipePipe implements PipeTransform {

  transform(name:string): string {
    let name_parts = name.split(' ');
    if(name_parts.length <= 2) return name;
    
    let abbreviate_name = '';
    for (let i = 0; i < name_parts.length; i++) {
      if(i == 0) {
        abbreviate_name += name_parts[i] + ' ';
        continue;
      }
      if(name_parts[i] == 'de' || name_parts[i] == 'da' || name_parts[i] == 'do') continue;
      if(i == name_parts.length - 1) {
        abbreviate_name += name_parts[i];
        continue;
      }
      abbreviate_name += name_parts[i][0] + '. ';
    }

    return abbreviate_name;
  }

}
