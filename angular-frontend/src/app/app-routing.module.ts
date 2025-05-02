import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Autenticación
import { LoginComponent } from './auth/login/login.component';
import { RecuperarComponent } from './auth/recuperar/recuperar.component';
import { VerificarCodigoComponent } from './auth/verificar-codigo/verificar-codigo.component';
import { NuevaContrasenaComponent } from './auth/nueva-contrasena/nueva-contrasena.component';

// Administración
import { PanelAdminComponent } from './admin/panel-admin/panel-admin.component';
import { CrearUsuarioComponent } from './admin/crear-usuario/crear-usuario.component';
import { EditarUsuarioComponent } from './admin/editar-usuario/editar-usuario.component';
import { EliminarUsuarioComponent } from './admin/eliminar-usuario/eliminar-usuario.component';
import { BuscarUsuarioComponent } from './admin/buscar-usuario/buscar-usuario.component';
import { GestionUsuariosComponent } from './admin/gestion-usuarios/gestion-usuarios.component';

// Gestor
import { PanelGestorComponent } from './gestor/panel-gestor/panel-gestor.component';
import { ReportesComponent } from './gestor/reportes/reportes.component';
import { MensajesComponent } from './gestor/mensajes/mensajes.component';
import { ListaEstudiantesComponent } from './gestor/estudiantes/lista-estudiantes.component';
import { PanelFormularioComponent } from './gestor/panel-formulario/panel-formulario.component';
import { CrearFormularioComponent } from './gestor/crear-formulario/crear-formulario.component';
import { VerFormularioComponent } from './gestor/ver-formulario/ver-formulario.component';

// Estudiantes
import { FormularioDesercionComponent } from './estudiante/formulario-desercion/formulario-desercion.component';
import { FormularioDesercionexitComponent } from './estudiante/formulario-desercionexit/formulario-desercionexit.component';

// Guards
import { AuthGuard } from './core/guards/auth.guard';
import { RoleGuard } from './core/guards/role.guard';

const routes: Routes = [
  // Autenticación
  { path: 'login', component: LoginComponent },
  { path: 'recuperar', component: RecuperarComponent },
  { path: 'verificar-codigo', component: VerificarCodigoComponent },
  { path: 'nueva-contrasena', component: NuevaContrasenaComponent },

  // Administración - Solo rol 1 (Admin)
  { 
    path: 'admin', 
    component: PanelAdminComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [1] } 
  },
  { 
    path: 'admin/usuarios', 
    component: GestionUsuariosComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [1] } 
  },
  { 
    path: 'admin/usuarios/crear', 
    component: CrearUsuarioComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [1] } 
  },
  { 
    path: 'admin/usuarios/editar/:id', 
    component: EditarUsuarioComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [1] } 
  },
  { 
    path: 'admin/usuarios/eliminar', 
    component: EliminarUsuarioComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [1] } 
  },
  { 
    path: 'admin/usuarios/buscar', 
    component: BuscarUsuarioComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [1] } 
  },

  // Gestor - Solo rol 2 (Gestor)
  { 
    path: 'gestor', 
    component: PanelGestorComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [2] } 
  },
  { 
    path: 'gestor/reportes', 
    component: ReportesComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [2] } 
  },
  { 
    path: 'gestor/mensajes', 
    component: MensajesComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [2] } 
  },
  {
    path: 'gestor/estudiantes', 
    component: ListaEstudiantesComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [2] } 
  },
  // Rutas para la gestión de formularios - Solo gestor
  { 
    path: 'gestor/formularios', 
    component: PanelFormularioComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [2] } 
  },
  { 
    path: 'gestor/formularios/crear', 
    component: CrearFormularioComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [2] } 
  },
  { 
    path: 'gestor/formularios/ver', 
    component: VerFormularioComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [2] } 
  },
  { 
    path: 'gestor/formularios/ver/:id', 
    component: VerFormularioComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [2] } 
  },
  { 
    path: 'gestor/formularios/editar/:id', 
    component: CrearFormularioComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [2] } 
  },

  // Estudiante - Solo rol 3 (Estudiante)
  { 
    path: 'formulario-desercion', 
    component: FormularioDesercionComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [3] } 
  },
  { 
    path: 'formulario-desercion/exito', 
    component: FormularioDesercionexitComponent,
    canActivate: [AuthGuard, RoleGuard], 
    data: { roles: [3] } 
  },

  // Rutas por defecto y wildcard
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/login' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}