import { NgModule } from '@angular/core';
import {CommonModule, NgOptimizedImage} from '@angular/common';
import { HomeComponent } from './components/home/home.component';
import {HomeRoutingModule} from "./home-routing.module";
import { NavigationComponent } from './components/navigation/navigation.component';



@NgModule({
  declarations: [
    HomeComponent,
    NavigationComponent,
  ],
  imports: [
    CommonModule,
    HomeRoutingModule,
    NgOptimizedImage
  ]
})
export class HomeModule {}
