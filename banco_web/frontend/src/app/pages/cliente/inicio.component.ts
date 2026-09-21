import { CurrencyPipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { BancoApiService, Conta } from '../../core/banco-api.service';

@Component({
  selector: 'app-cliente-inicio',
  imports: [CurrencyPipe, RouterLink],
  template: `
    <h1>Painel do correntista</h1>
    <p class="muted">Resumo das contas vinculadas ao seu cadastro.</p>
    <div class="cards">
      @for (conta of contas(); track conta.numero) {
        <a class="kpi" [routerLink]="['/internet-banking/contas', conta.numero]">
          <span>Conta {{ conta.numero }} · {{ conta.tipo }}</span>
          <strong>{{ conta.saldo | currency: 'BRL' }}</strong>
        </a>
      }
    </div>
    @if (!contas().length) {
      <p class="aviso-box">Nenhuma conta vinculada a este usuário.</p>
    }
  `,
})
export class ClienteInicioComponent implements OnInit {
  private api = inject(BancoApiService);
  contas = signal<Conta[]>([]);

  ngOnInit() {
    this.api.minhasContas().subscribe((c) => this.contas.set(c));
  }
}
