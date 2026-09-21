import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BancoApiService, Usuario } from '../../core/banco-api.service';

@Component({
  selector: 'app-usuarios',
  imports: [FormsModule],
  template: `
    <h1>Usuários e papéis</h1>
    <form class="card-form" (ngSubmit)="criar()">
      <h3>Novo usuário</h3>
      <label>Usuário <input [(ngModel)]="usuario" name="usuario" required /></label>
      <label>Senha <input [(ngModel)]="senha" name="senha" required /></label>
      <label>Papel
        <select [(ngModel)]="papel" name="papel">
          <option value="cliente">cliente</option>
          <option value="operador">operador</option>
          <option value="admin">admin</option>
        </select>
      </label>
      <label>CPF do cliente (opcional)
        <input [(ngModel)]="clienteCpf" name="cpf" />
      </label>
      <button type="submit">Criar</button>
      @if (erro()) { <p class="erro">{{ erro() }}</p> }
    </form>
    <table>
      <thead><tr><th>Usuário</th><th>Papel</th><th>CPF vinculado</th></tr></thead>
      <tbody>
        @for (u of usuarios(); track u.usuario) {
          <tr>
            <td>{{ u.usuario }}</td>
            <td>{{ u.papel }}</td>
            <td>{{ u.cliente_cpf || '—' }}</td>
          </tr>
        }
      </tbody>
    </table>
  `,
})
export class UsuariosComponent implements OnInit {
  private api = inject(BancoApiService);
  usuarios = signal<Usuario[]>([]);
  usuario = '';
  senha = '';
  papel = 'cliente';
  clienteCpf = '';
  erro = signal('');

  ngOnInit() {
    this.carregar();
  }

  carregar() {
    this.api.usuarios().subscribe((u) => this.usuarios.set(u));
  }

  criar() {
    this.api.criarUsuario(this.usuario, this.senha, this.papel, this.clienteCpf || null).subscribe({
      next: () => {
        this.usuario = '';
        this.senha = '';
        this.carregar();
      },
      error: (e) => this.erro.set(e.error?.detail || 'Não foi possível criar o usuário.'),
    });
  }
}
