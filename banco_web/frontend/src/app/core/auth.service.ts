import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs';

export interface Sessao {
  ok?: boolean;
  usuario: string;
  papel: string;
  cliente_cpf: string | null;
  token: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  sessao = signal<Sessao | null>(this.lerSessao());

  constructor(
    private http: HttpClient,
    private router: Router,
  ) {}

  private lerSessao(): Sessao | null {
    const bruto = localStorage.getItem('nb_sessao');
    if (!bruto) {
      return null;
    }
    try {
      return JSON.parse(bruto) as Sessao;
    } catch {
      return null;
    }
  }

  private gravar(sessao: Sessao) {
    localStorage.setItem('nb_token', sessao.token);
    localStorage.setItem('nb_sessao', JSON.stringify(sessao));
    this.sessao.set(sessao);
  }

  loginCliente(usuario: string, senha: string) {
    return this.http.post<Sessao>('/api/auth/login', { usuario, senha }).pipe(
      tap((s) => this.gravar(s)),
    );
  }

  loginCorporativo(usuario: string, senha: string) {
    return this.http.post<Sessao>('/api/auth/backoffice/login', { usuario, senha }).pipe(
      tap((s) => this.gravar(s)),
    );
  }

  sair() {
    this.http.post('/api/auth/logout', {}).subscribe({ complete: () => undefined });
    localStorage.removeItem('nb_token');
    localStorage.removeItem('nb_sessao');
    this.sessao.set(null);
    void this.router.navigateByUrl('/');
  }

  ehCliente() {
    return this.sessao()?.papel === 'cliente';
  }

  ehStaff() {
    const papel = this.sessao()?.papel;
    return papel === 'operador' || papel === 'admin';
  }

  ehAdmin() {
    return this.sessao()?.papel === 'admin';
  }
}
