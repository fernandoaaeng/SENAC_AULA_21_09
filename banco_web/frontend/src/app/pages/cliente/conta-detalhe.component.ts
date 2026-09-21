import { CurrencyPipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { BancoApiService, Conta } from '../../core/banco-api.service';

@Component({
  selector: 'app-cliente-conta-detalhe',
  imports: [CurrencyPipe, FormsModule, RouterLink],
  template: `
    <a routerLink="/internet-banking/contas" class="back">Todas as contas</a>
    @if (conta(); as c) {
      <h1>Conta {{ c.numero }}</h1>
      <p class="muted">{{ c.tipo }} · titular {{ c.titular }}</p>
      <p class="saldo">{{ c.saldo | currency: 'BRL' }}</p>
      <form class="row-form" (ngSubmit)="depositar()">
        <input type="number" step="0.01" [(ngModel)]="valorDeposito" name="dep" placeholder="Depósito" />
        <button type="submit">Depositar</button>
      </form>
      <form class="row-form" (ngSubmit)="sacar()">
        <input type="number" step="0.01" [(ngModel)]="valorSaque" name="saq" placeholder="Saque" />
        <button class="warn" type="submit">Sacar</button>
      </form>
      @if (c.tipo === 'poupanca') {
        <button type="button" class="ghost-btn" (click)="render()">Aplicar rendimento</button>
      }
    }
    @if (erro()) {
      <p class="erro">{{ erro() }}</p>
    }
  `,
})
export class ClienteContaDetalheComponent implements OnInit {
  private api = inject(BancoApiService);
  private rota = inject(ActivatedRoute);
  conta = signal<Conta | null>(null);
  erro = signal('');
  valorDeposito = 0;
  valorSaque = 0;
  numero = 0;

  ngOnInit() {
    this.numero = Number(this.rota.snapshot.paramMap.get('numero'));
    this.carregar();
  }

  carregar() {
    this.api.minhaConta(this.numero).subscribe({
      next: (c) => this.conta.set(c),
      error: (e) => this.erro.set(e.error?.detail || 'Conta indisponível.'),
    });
  }

  depositar() {
    this.api.meuDeposito(this.numero, this.valorDeposito).subscribe({
      next: (c) => this.conta.set(c),
      error: (e) => this.erro.set(e.error?.detail || 'Falha no depósito.'),
    });
  }

  sacar() {
    this.api.meuSaque(this.numero, this.valorSaque).subscribe({
      next: (c) => this.conta.set(c),
      error: (e) => this.erro.set(e.error?.detail || 'Falha no saque.'),
    });
  }

  render() {
    this.api.meuRendimento(this.numero).subscribe({
      next: () => this.carregar(),
      error: (e) => this.erro.set(e.error?.detail || 'Falha no rendimento.'),
    });
  }
}
