import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BancoApiService, Cliente } from '../../core/banco-api.service';

@Component({
  selector: 'app-clientes',
  imports: [FormsModule],
  template: `
    <h1>Clientes</h1>
    <form class="card-form" (ngSubmit)="cadastrar()">
      <h3>Novo cliente</h3>
      <label>Nome <input [(ngModel)]="nome" name="nome" required /></label>
      <label>CPF <input [(ngModel)]="cpf" name="cpf" required /></label>
      <button type="submit">Cadastrar</button>
      @if (erro()) { <p class="erro">{{ erro() }}</p> }
    </form>
    <table>
      <thead><tr><th>Nome</th><th>CPF</th></tr></thead>
      <tbody>
        @for (c of clientes(); track c.cpf) {
          <tr><td>{{ c.nome }}</td><td>{{ c.cpf }}</td></tr>
        }
      </tbody>
    </table>
  `,
})
export class ClientesComponent implements OnInit {
  private api = inject(BancoApiService);
  clientes = signal<Cliente[]>([]);
  nome = '';
  cpf = '';
  erro = signal('');

  ngOnInit() {
    this.carregar();
  }

  carregar() {
    this.api.clientes().subscribe((c) => this.clientes.set(c));
  }

  cadastrar() {
    this.erro.set('');
    this.api.criarCliente(this.nome, this.cpf).subscribe({
      next: () => {
        this.nome = '';
        this.cpf = '';
        this.carregar();
      },
      error: (e) => this.erro.set(e.error?.detail || 'Não foi possível cadastrar.'),
    });
  }
}
