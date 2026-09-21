import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-login-corporativo',
  imports: [FormsModule, RouterLink],
  template: `
    <div class="auth-layout corporativo">
      <aside>
        <div class="brand light">
          <span class="mark">NB</span>
          <div>
            <strong>NexusBank</strong>
            <small>Backoffice</small>
          </div>
        </div>
        <h2>Portal do colaborador</h2>
        <p>Restrito a operadores e administradores da mesa de cadastro e compliance.</p>
      </aside>
      <main class="auth-card">
        <a routerLink="/" class="back">Voltar ao início</a>
        <h1>Acesso corporativo</h1>
        <form (ngSubmit)="entrar()">
          <label>Usuário institucional
            <input name="usuario" [(ngModel)]="usuario" autocomplete="username" required />
          </label>
          <label>Senha
            <input name="senha" type="password" [(ngModel)]="senha" autocomplete="current-password" required />
          </label>
          @if (erro()) {
            <p class="erro">{{ erro() }}</p>
          }
          <button type="submit" [disabled]="carregando()">Entrar no backoffice</button>
        </form>
        <p class="hint">Correntista? <a routerLink="/login">Internet Banking</a></p>
      </main>
    </div>
  `,
})
export class LoginCorporativoComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  usuario = '';
  senha = '';
  erro = signal('');
  carregando = signal(false);

  entrar() {
    this.erro.set('');
    this.carregando.set(true);
    this.auth.loginCorporativo(this.usuario, this.senha).subscribe({
      next: () => void this.router.navigateByUrl('/backoffice'),
      error: (e) => {
        this.carregando.set(false);
        this.erro.set(e.error?.detail || 'Acesso corporativo recusado.');
      },
    });
  }
}
