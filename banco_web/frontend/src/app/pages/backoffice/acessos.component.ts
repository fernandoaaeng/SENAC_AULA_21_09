import { Component, inject, OnInit, signal } from '@angular/core';
import { BancoApiService, LogAcesso } from '../../core/banco-api.service';

@Component({
  selector: 'app-acessos',
  template: `
    <h1>Logs de acesso</h1>
    <p class="muted">Tentativas de autenticação registradas no PostgreSQL.</p>
    <table>
      <thead>
        <tr><th>Quando</th><th>Usuário</th><th>Sucesso</th><th>IP</th></tr>
      </thead>
      <tbody>
        @for (l of logs(); track $index) {
          <tr>
            <td>{{ l.criado_em }}</td>
            <td>{{ l.usuario }}</td>
            <td>{{ l.sucesso ? 'sim' : 'não' }}</td>
            <td>{{ l.ip }}</td>
          </tr>
        }
      </tbody>
    </table>
  `,
})
export class AcessosComponent implements OnInit {
  private api = inject(BancoApiService);
  logs = signal<LogAcesso[]>([]);

  ngOnInit() {
    this.api.logs().subscribe((l) => this.logs.set(l));
  }
}
