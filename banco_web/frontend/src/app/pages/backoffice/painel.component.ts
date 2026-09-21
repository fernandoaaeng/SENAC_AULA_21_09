import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-painel',
  imports: [RouterLink],
  template: `
    <h1>Painel operacional</h1>
    <p class="muted">Áreas liberadas para o perfil {{ auth.sessao()?.papel }}.</p>
    <div class="cards">
      <a class="kpi" routerLink="/backoffice/clientes">Cadastro de clientes</a>
      <a class="kpi" routerLink="/backoffice/contas">Contas e movimentação</a>
      @if (auth.ehAdmin()) {
        <a class="kpi" routerLink="/backoffice/acessos">Auditoria de login</a>
        <a class="kpi" routerLink="/backoffice/sessoes">Sessões ativas</a>
      }
    </div>
  `,
})
export class PainelComponent {
  auth = inject(AuthService);
}
