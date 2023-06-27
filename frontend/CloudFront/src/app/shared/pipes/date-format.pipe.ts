import { Pipe, PipeTransform } from '@angular/core';
import * as moment from 'moment';

@Pipe({
  name: 'dateFormat'
})
export class DateFormatPipe implements PipeTransform {

  transform(value: string): string {
    if (value =='-') {
      return "-";
    }

    return moment(value).format('MMM D, YYYY - h:mm A');
  }
}
