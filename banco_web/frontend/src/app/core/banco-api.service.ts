import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface Conta {
  numero: number;
  titular: string;
  cpf: string;
  tipo: string;
  saldo: number;
  limite: number;
}

export interface Cliente {
  nome: string;
  cpf: string;
}

export interface LogAcesso {
  usuario: string;
  sucesso: number;
  ip: string;
  criado_em: string;
}

export interface SessaoAtiva {
  token: string;
  usuario: string;
  papel: string;
  ip: string;
  criado_em: string;
}

export interface Usuario {
  usuario: string;
  papel: string;
  cliente_cpf: string | null;
}

@Injectable({ providedIn: 'root' })
export class BancoApiService {
  constructor(private http: HttpClient) {}

  minhasContas() {
    return this.http.get<Conta[]>('/api/me/contas');
  }

  minhaConta(numero: number) {
    return this.http.get<Conta>(`/api/me/contas/${numero}`);
  }

  meuDeposito(numero: number, valor: number) {
    return this.http.post<Conta>(`/api/me/contas/${numero}/depositar`, { valor });
  }

  meuSaque(numero: number, valor: number) {
    return this.http.post<Conta>(`/api/me/contas/${numero}/sacar`, { valor });
  }

  meuRendimento(numero: number) {
    return this.http.post(`/api/me/contas/${numero}/render`, {});
  }

  clientes() {
    return this.http.get<Cliente[]>('/api/clientes');
  }

  criarCliente(nome: string, cpf: string) {
    return this.http.post<Cliente>('/api/clientes', { nome, cpf });
  }

  contas() {
    return this.http.get<Conta[]>('/api/contas');
  }

  criarConta(cpf: string, tipo: 'p' | 'c', saldo_inicial: number) {
    return this.http.post<Conta>('/api/contas', { cpf, tipo, saldo_inicial });
  }

  depositar(numero: number, valor: number) {
    return this.http.post<Conta>(`/api/contas/${numero}/depositar`, { valor });
  }

  sacar(numero: number, valor: number) {
    return this.http.post<Conta>(`/api/contas/${numero}/sacar`, { valor });
  }

  render(numero: number) {
    return this.http.post(`/api/contas/${numero}/render`, {});
  }

  excluirConta(numero: number) {
    return this.http.delete(`/api/contas/${numero}`);
  }

  logs() {
    return this.http.get<LogAcesso[]>('/api/admin/logs');
  }

  sessoes() {
    return this.http.get<SessaoAtiva[]>('/api/admin/sessoes');
  }

  usuarios() {
    return this.http.get<Usuario[]>('/api/admin/usuarios');
  }

  criarUsuario(usuario: string, senha: string, papel: string, cliente_cpf: string | null) {
    return this.http.post('/api/admin/usuarios', { usuario, senha, papel, cliente_cpf });
  }
}
