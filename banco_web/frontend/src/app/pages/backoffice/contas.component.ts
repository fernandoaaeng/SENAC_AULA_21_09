import { CurrencyPipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/auth.service';
import { BancoApiService, Conta } from '../../core/banco-api.service';

@Component({
  selector: 'app-contas',
  imports: [CurrencyPipe, FormsModule],
  template: `
    <h1>Contas</h1>
    <form class="card-form" (ngSubmit)="criar()">
      <h3>Abrir conta</h3>
      <label>CPF <input [(ngModel)]="cpf" name="cpf" required /></label>
      <label>Tipo
        <select [(ngModel)]="tipo" name="tipo">
          <option value="p">Poupança</option>
          <option value="c">Corrente</option>
        </select>
      </label>
      <label>Saldo inicial <input type="number" step="0.01" [(ngModel)]="saldo" name="saldo" required /></label>
      <button type="submit">Criar</button>
    </form>
    @if (erro()) { <p class="erro">{{ erro() }}</p> }
    <table>
      <thead>
        <tr>
          <th>Número</th><th>Titular</th><th>CPF</th><th>Tipo</th><th>Saldo</th><th>Ações</th>
        </tr>
      </thead>
      <tbody>
        @for (c of contas(); track c.numero) {
          <tr>
            <td>{{ c.numero }}</td>
            <td>{{ c.titular }}</td>
            <td>{{ c.cpf }}</td>
            <td>{{ c.tipo }}</td>
            <td>{{ c.saldo | currency: 'BRL' }}</td>
            <td class="acoes">
              <button type="button" (click)="movimentar(c.numero, 'd')">Depósito</button>
              <button type="button" class="warn" (click)="movimentar(c.numero, 's')">Saque</button>
              @if (c.tipo === 'poupanca') {
                <button type="button" class="ghost-btn" (click)="render(c.numero)">Render</button>
              }
              @if (auth.ehAdmin()) {
                <button type="button" class="danger" (click)="excluir(c.numero)">Excluir</button>
              }
            </td>
          </tr>
        }
      </tbody>
    </table>
  `,
})
export class ContasComponent implements OnInit {
  private api = inject(BancoApiService);
  auth = inject(AuthService);
  contas = signal<Conta[]>([]);
  cpf = '';
  tipo: 'p' | 'c' = 'c';
  saldo = 0;
  erro = signal('');

  ngOnInit() {
    this.carregar();
  }

  carregar() {
    this.api.contas().subscribe((c) => this.contas.set(c));
  }

  criar() {
    this.api.criarConta(this.cpf, this.tipo, this.saldo).subscribe({
      next: () => this.carregar(),
      error: (e) => this.erro.set(e.error?.detail || 'Falha ao criar conta.'),
    });
  }

  movimentar(numero: number, tipo: 'd' | 's') {
    const bruto = prompt(tipo === 'd' ? 'Valor do depósito' : 'Valor do saque');
    if (bruto === null) return;
    const valor = Number(bruto);
    const req = tipo === 'd' ? this.api.depositar(numero, valor) : this.api.sacar(numero, valor);
    req.subscribe({
      next: () => this.carregar(),
      error: (e) => this.erro.set(e.error?.detail || 'Operação recusada.'),
    });
  }

  render(numero: number) {
    this.api.render(numero).subscribe({
      next: () => this.carregar(),
      error: (e) => this.erro.set(e.error?.detail || 'Falha no rendimento.'),
    });
  }

  excluir(numero: number) {
    this.api.excluirConta(numero).subscribe({
      next: () => this.carregar(),
      error: (e) => this.erro.set(e.error?.detail || 'Exclusão recusada.'),
    });
  }
}
