import { CurrencyPipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { BancoApiService, Conta } from '../../core/banco-api.service';

@Component({
  selector: 'app-cliente-contas',
  imports: [CurrencyPipe, RouterLink],
  template: `
    <h1>Minhas contas</h1>
    <table>
      <thead>
        <tr>
          <th>Número</th>
          <th>Tipo</th>
          <th>Saldo</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        @for (conta of contas(); track conta.numero) {
          <tr>
            <td>{{ conta.numero }}</td>
            <td>{{ conta.tipo }}</td>
            <td>{{ conta.saldo | currency: 'BRL' }}</td>
            <td><a [routerLink]="['/internet-banking/contas', conta.numero]">Movimentar</a></td>
          </tr>
        }
      </tbody>
    </table>
  `,
})
export class ClienteContasComponent implements OnInit {
  private api = inject(BancoApiService);
  contas = signal<Conta[]>([]);

  ngOnInit() {
    this.api.minhasContas().subscribe((c) => this.contas.set(c));
  }
}
