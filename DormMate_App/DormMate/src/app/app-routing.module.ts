import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PrimaryComponent } from './components/primary/primary.component';
import { AdminComponent } from './component/admin/admin.component';
import { CreateAccountComponent } from './component/create-account/create-account.component';
import { MatchComponent } from './component/match/match.component';
import { EditProfileComponent } from './component/edit-profile/edit-profile.component';
import { ProfileComponent } from './component/profile/profile.component';
import { MessagingComponent } from './component/messaging/messaging.component';

const routes: Routes = [
	{path: 'admin', component: AdminComponent},
	{path: '', component: PrimaryComponent},
	{path: 'createAccount', component: CreateAccountComponent},
	{path: 'match', component: MatchComponent},
	{path: 'editProfile', component: EditProfileComponent},
	{path: 'profile', component: ProfileComponent},
	{path: 'messages', component: MessagingComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [AdminComponent, PrimaryComponent, CreateAccountComponent, MatchComponent, EditProfileComponent, ProfileComponent, MessagingComponent]
