import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-login',
  imports: [FormsModule, RouterLink],
  template: `
    <div class="auth-layout">
      <aside>
        <div class="brand light">
          <span class="mark">NB</span>
          <div>
            <strong>NexusBank</strong>
            <small>Internet Banking</small>
          </div>
        </div>
        <h2>Acesso do correntista</h2>
        <p>Use o canal de pessoas físicas. Colaboradores devem entrar pelo portal corporativo.</p>
      </aside>
      <main class="auth-card">
        <a routerLink="/" class="back">Voltar ao início</a>
        <h1>Entrar</h1>
        <form (ngSubmit)="entrar()">
          <label>Usuário
            <input name="usuario" [(ngModel)]="usuario" autocomplete="username" required />
          </label>
          <label>Senha
            <input name="senha" type="password" [(ngModel)]="senha" autocomplete="current-password" required />
          </label>
          @if (erro()) {
            <p class="erro">{{ erro() }}</p>
          }
          <button type="submit" [disabled]="carregando()">Acessar conta</button>
        </form>
        <p class="hint">Colaborador? <a routerLink="/acesso-corporativo">Acesso corporativo</a></p>
      </main>
    </div>
  `,
})
export class LoginComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  usuario = '';
  senha = '';
  erro = signal('');
  carregando = signal(false);

  entrar() {
    this.erro.set('');
    this.carregando.set(true);
    this.auth.loginCliente(this.usuario, this.senha).subscribe({
      next: () => void this.router.navigateByUrl('/internet-banking'),
      error: (e) => {
        this.carregando.set(false);
        this.erro.set(e.error?.detail || 'Não foi possível autenticar.');
      },
    });
  }
}
