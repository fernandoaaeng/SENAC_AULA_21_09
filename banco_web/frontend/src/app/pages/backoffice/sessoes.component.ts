import { Component, inject, OnInit, signal } from '@angular/core';
import { BancoApiService, SessaoAtiva } from '../../core/banco-api.service';

@Component({
  selector: 'app-sessoes',
  template: `
    <h1>Sessões ativas</h1>
    <p class="muted">Tokens emitidos após o login. O valor completo aparece na tabela.</p>
    <table>
      <thead>
        <tr><th>Usuário</th><th>Papel</th><th>IP</th><th>Criado em</th><th>Token</th></tr>
      </thead>
      <tbody>
        @for (s of sessoes(); track s.token) {
          <tr>
            <td>{{ s.usuario }}</td>
            <td>{{ s.papel }}</td>
            <td>{{ s.ip }}</td>
            <td>{{ s.criado_em }}</td>
            <td class="mono">{{ s.token }}</td>
          </tr>
        }
      </tbody>
    </table>
  `,
})
export class SessoesComponent implements OnInit {
  private api = inject(BancoApiService);
  sessoes = signal<SessaoAtiva[]>([]);

  ngOnInit() {
    this.api.sessoes().subscribe((s) => this.sessoes.set(s));
  }
}
