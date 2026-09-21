import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-home',
  imports: [RouterLink],
  template: `
    <div class="public-shell">
      <header class="topbar">
        <div class="brand">
          <span class="mark">NB</span>
          <div>
            <strong>NexusBank</strong>
            <small>Corporate Banking</small>
          </div>
        </div>
        <nav class="top-links">
          <a routerLink="/login">Internet Banking</a>
          <a class="ghost" routerLink="/acesso-corporativo">Acesso corporativo</a>
        </nav>
      </header>

      <section class="hero">
        <p class="kicker">Plataforma institucional</p>
        <h1>Internet Banking para clientes e backoffice para a operação.</h1>
        <p class="lead">
          Acesse contas, movimentações e cadastros em áreas separadas, com perfil de cliente,
          operador ou administrador.
        </p>
        <div class="cta">
          <a class="btn" routerLink="/login">Entrar no Internet Banking</a>
          <a class="btn secondary" routerLink="/acesso-corporativo">Portal do colaborador</a>
        </div>
      </section>

      <section class="grid-3">
        <article>
          <h3>Clientes</h3>
          <p>Consulta de saldo, depósito, saque e rendimento de poupança na área autenticada.</p>
        </article>
        <article>
          <h3>Operação</h3>
          <p>Cadastro de clientes e contas no backoffice, com papéis distintos.</p>
        </article>
        <article>
          <h3>Governança</h3>
          <p>Administradores acompanham sessões ativas, usuários e tentativas de acesso.</p>
        </article>
      </section>
    </div>
  `,
})
export class HomeComponent {}
