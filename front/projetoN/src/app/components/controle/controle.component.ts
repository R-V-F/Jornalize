import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-controle',
  templateUrl: './controle.component.html',
  styleUrls: ['./controle.component.css']
})
export class ControleComponent {
  @Output() dataToParent = new EventEmitter<number>();
  @Output() dataToParentBool = new EventEmitter<boolean>();

  isChecked = true;
  number_of_columns = 4;
  showSettings = false;
  bypass = false;

  public addColumn() {
    this.number_of_columns++;
    this.dataToParent.emit(this.number_of_columns);
  }
  public removeColumn() {
    this.number_of_columns--;
    this.dataToParent.emit(this.number_of_columns);
  }
  public toggleSettings() {
    this.showSettings = !this.showSettings;
  }
  public toggleBypass() {
    this.bypass = !this.bypass;
    this.dataToParentBool.emit(this.bypass);
  }
}
