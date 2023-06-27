import { Injectable } from '@angular/core';
import {NavItem} from "../models/nav-item";

@Injectable({
  providedIn: 'root'
})
export class NavigationService {
  constructor() {}

  getNavItems(): NavItem[] {
    return [
      { routeLink: '/home/my-albums/', label: 'My Albums', icon: 'fa fa-solid fa-folder-open' },
      { routeLink: '/home/shared-with-me/', label: 'Shared With Me', icon: 'fa fa-user-group' }
    ];
  }
}
