import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { UserdataService } from './userdata.service';

import { AppRoutingModule, routingComponents } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { SocialLoginModule, AuthServiceConfig, FacebookLoginProvider } from 'angularx-social-login';
import {
  MatIconModule,
  MatButtonModule,
  MatCardModule } from '@angular/material';
//import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

const config = new AuthServiceConfig([
  {
    id: FacebookLoginProvider.PROVIDER_ID,
    provider: new FacebookLoginProvider('2374328789354785')
  }
]);

export function provideConfig() {
  return config;
}

@NgModule({
  declarations: [AppComponent, routingComponents],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    SocialLoginModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    ReactiveFormsModule
    //FontAwesomeModule
  ],
  providers: [
    {
      provide: AuthServiceConfig,
      useFactory: provideConfig
    },
    UserdataService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
