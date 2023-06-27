import {Component, EventEmitter, HostListener, OnInit, Output} from '@angular/core';
import {AuthService} from "../../../../core/services/auth.service";
import {Router} from "@angular/router";
import {NavItem} from "../../models/nav-item";
import {NavigationService} from "../../services/navigation.service";

interface SideNavToggle {
  screenWidth: number;
  collapsed: boolean;
}

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit {
  @Output() onToggleSideNav: EventEmitter<SideNavToggle> = new EventEmitter();
  hideMenu: boolean = false;
  screenWidth = 0;

  navItems: NavItem[] = [];

  constructor(private authService: AuthService,
              private router: Router,
              private navigationService: NavigationService) {
  }

  ngOnInit(): void {
    this.navItems = this.navigationService.getNavItems();
    this.screenWidth = window.innerWidth;
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any) {
    this.screenWidth = window.innerWidth;
    if (this.screenWidth <= 768) {
      this.hideMenu = true;
      this.onToggleSideNav.emit({collapsed: this.hideMenu, screenWidth: this.screenWidth});
    }
  }

  toggleMenu() {
    this.hideMenu = !this.hideMenu;
  }

  logOut() {
    this.authService.logout();
    this.router.navigate(['/login-register']);
  }
}
