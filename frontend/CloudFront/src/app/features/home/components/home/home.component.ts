import {Component, OnInit, ViewChild} from '@angular/core';
import {NavigationComponent} from "../navigation/navigation.component";
import {AuthService} from "../../../../core/services/auth.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  @ViewChild(NavigationComponent) navigationComponent!: NavigationComponent;

  contentExpanded: boolean = false;
  username: string | null = null;

  constructor(private authService: AuthService) {
  }

  ngOnInit(): void {
    this.username = this.authService.getUsernameFromToken();
  }

  toggleMenu() {
    this.navigationComponent.toggleMenu();
    this.contentExpanded = !this.contentExpanded;
  }

  onToggleSideNav($event: any) {
    this.contentExpanded = true;
  }
}
