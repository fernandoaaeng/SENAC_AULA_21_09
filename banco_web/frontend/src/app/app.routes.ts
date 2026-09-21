import { Routes } from '@angular/router';
import { adminGuard, clienteGuard, staffGuard } from './core/auth.guard';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/home.component').then((m) => m.HomeComponent) },
  { path: 'login', loadComponent: () => import('./pages/login.component').then((m) => m.LoginComponent) },
  {
    path: 'acesso-corporativo',
    loadComponent: () => import('./pages/login-corporativo.component').then((m) => m.LoginCorporativoComponent),
  },
  {
    path: 'internet-banking',
    canActivate: [clienteGuard],
    loadComponent: () => import('./pages/cliente/shell.component').then((m) => m.ClienteShellComponent),
    children: [
      { path: '', loadComponent: () => import('./pages/cliente/inicio.component').then((m) => m.ClienteInicioComponent) },
      { path: 'contas', loadComponent: () => import('./pages/cliente/contas.component').then((m) => m.ClienteContasComponent) },
      {
        path: 'contas/:numero',
        loadComponent: () => import('./pages/cliente/conta-detalhe.component').then((m) => m.ClienteContaDetalheComponent),
      },
    ],
  },
  {
    path: 'backoffice',
    canActivate: [staffGuard],
    loadComponent: () => import('./pages/backoffice/shell.component').then((m) => m.BackofficeShellComponent),
    children: [
      { path: '', loadComponent: () => import('./pages/backoffice/painel.component').then((m) => m.PainelComponent) },
      { path: 'clientes', loadComponent: () => import('./pages/backoffice/clientes.component').then((m) => m.ClientesComponent) },
      { path: 'contas', loadComponent: () => import('./pages/backoffice/contas.component').then((m) => m.ContasComponent) },
      {
        path: 'acessos',
        canActivate: [adminGuard],
        loadComponent: () => import('./pages/backoffice/acessos.component').then((m) => m.AcessosComponent),
      },
      {
        path: 'sessoes',
        canActivate: [adminGuard],
        loadComponent: () => import('./pages/backoffice/sessoes.component').then((m) => m.SessoesComponent),
      },
      {
        path: 'usuarios',
        canActivate: [adminGuard],
        loadComponent: () => import('./pages/backoffice/usuarios.component').then((m) => m.UsuariosComponent),
      },
    ],
  },
  { path: '**', redirectTo: '' },
];
