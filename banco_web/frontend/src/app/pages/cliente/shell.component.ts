import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-cliente-shell',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="app-shell">
      <aside class="sidebar">
        <div class="brand light">
          <span class="mark">NB</span>
          <div>
            <strong>NexusBank</strong>
            <small>Internet Banking</small>
          </div>
        </div>
        <nav>
          <a routerLink="/internet-banking" routerLinkActive="on" [routerLinkActiveOptions]="{ exact: true }">Início</a>
          <a routerLink="/internet-banking/contas" routerLinkActive="on">Minhas contas</a>
        </nav>
        <button class="sair" type="button" (click)="auth.sair()">Encerrar sessão</button>
      </aside>
      <section class="content">
        <header class="content-head">
          <div>
            <p class="muted">Sessão autenticada</p>
            <h2>{{ auth.sessao()?.usuario }}</h2>
          </div>
          <span class="chip">perfil {{ auth.sessao()?.papel }}</span>
        </header>
        <router-outlet />
      </section>
    </div>
  `,
})
export class ClienteShellComponent {
  auth = inject(AuthService);
}
