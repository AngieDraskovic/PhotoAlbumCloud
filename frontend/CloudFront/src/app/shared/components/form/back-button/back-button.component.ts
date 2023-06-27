import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-back-button',
  templateUrl: './back-button.component.html',
  styleUrls: ['./back-button.component.css']
})
export class BackButtonComponent implements OnInit{
  @Input() buttonText!: string;
  @Output() onBack = new EventEmitter<void>();

  constructor() {
  }

  ngOnInit(): void {
  }

  back() {
    this.onBack.emit();
  }
}
