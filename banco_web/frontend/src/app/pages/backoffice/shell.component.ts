import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-backoffice-shell',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="app-shell dark">
      <aside class="sidebar">
        <div class="brand light">
          <span class="mark">NB</span>
          <div>
            <strong>NexusBank</strong>
            <small>Backoffice</small>
          </div>
        </div>
        <nav>
          <a routerLink="/backoffice" routerLinkActive="on" [routerLinkActiveOptions]="{ exact: true }">Painel</a>
          <a routerLink="/backoffice/clientes" routerLinkActive="on">Clientes</a>
          <a routerLink="/backoffice/contas" routerLinkActive="on">Contas</a>
          @if (auth.ehAdmin()) {
            <a routerLink="/backoffice/acessos" routerLinkActive="on">Logs de acesso</a>
            <a routerLink="/backoffice/sessoes" routerLinkActive="on">Sessões</a>
            <a routerLink="/backoffice/usuarios" routerLinkActive="on">Usuários</a>
          }
        </nav>
        <button class="sair" type="button" (click)="auth.sair()">Encerrar sessão</button>
      </aside>
      <section class="content">
        <header class="content-head">
          <div>
            <p class="muted">Mesa operacional</p>
            <h2>{{ auth.sessao()?.usuario }}</h2>
          </div>
          <span class="chip">{{ auth.sessao()?.papel }}</span>
        </header>
        <router-outlet />
      </section>
    </div>
  `,
})
export class BackofficeShellComponent {
  auth = inject(AuthService);
}
