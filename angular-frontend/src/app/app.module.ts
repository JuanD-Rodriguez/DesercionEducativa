import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { RouterModule } from '@angular/router';

import { JwtModule } from '@auth0/angular-jwt';

import { AppComponent } from './app.component';

// Interceptores
import { TokenInterceptor } from './core/services/interceptors/token.interceptor';

// Componentes de autenticación
import { LoginComponent } from './auth/login/login.component';
import { RecuperarComponent } from './auth/recuperar/recuperar.component';
import { VerificarCodigoComponent } from './auth/verificar-codigo/verificar-codigo.component';
import { NuevaContrasenaComponent } from './auth/nueva-contrasena/nueva-contrasena.component';

//Componentes de formularios
import { CrearFormularioComponent } from './gestor/crear-formulario/crear-formulario.component';
import { PanelFormularioComponent } from './gestor/panel-formulario/panel-formulario.component';
import { VerFormularioComponent } from './gestor/ver-formulario/ver-formulario.component';
// Importaremos MetricasFormularioComponent después

// Componentes de administración
import { PanelAdminComponent } from './admin/panel-admin/panel-admin.component';
import { CrearUsuarioComponent } from './admin/crear-usuario/crear-usuario.component';
import { EditarUsuarioComponent } from './admin/editar-usuario/editar-usuario.component';
import { EliminarUsuarioComponent } from './admin/eliminar-usuario/eliminar-usuario.component';
import { BuscarUsuarioComponent } from './admin/buscar-usuario/buscar-usuario.component';
import { GestionUsuariosComponent } from './admin/gestion-usuarios/gestion-usuarios.component';

// Componentes de gestor
import { PanelGestorComponent } from './gestor/panel-gestor/panel-gestor.component';
import { ReportesComponent } from './gestor/reportes/reportes.component';
import { MensajesComponent } from './gestor/mensajes/mensajes.component';
import { ListaEstudiantesComponent } from './gestor/estudiantes/lista-estudiantes.component';

// Componentes de estudiante
import { FormularioDesercionComponent } from './estudiante/formulario-desercion/formulario-desercion.component';
import { FormularioDesercionexitComponent } from './estudiante/formulario-desercionexit/formulario-desercionexit.component';

export function tokenGetter() {
  return localStorage.getItem('token');
}

@NgModule({
  declarations: [
    AppComponent,
    // Autenticación
    LoginComponent,
    RecuperarComponent,
    VerificarCodigoComponent,
    NuevaContrasenaComponent,
    
    // Administración
    PanelAdminComponent,
    CrearUsuarioComponent,
    EditarUsuarioComponent,
    EliminarUsuarioComponent,
    BuscarUsuarioComponent,
    GestionUsuariosComponent,
    
    // Gestor
    PanelGestorComponent,
    ReportesComponent,
    MensajesComponent,
    ListaEstudiantesComponent,
    
    // Formularios
    CrearFormularioComponent,
    PanelFormularioComponent,
    VerFormularioComponent,
    // MetricasFormularioComponent lo añadiremos después
    
    // Estudiante
    FormularioDesercionComponent,
    FormularioDesercionexitComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,         // Necesario para ngModel
    ReactiveFormsModule, // Necesario para formGroup
    HttpClientModule,
    AppRoutingModule,    // Necesario para routerLink
    RouterModule,        // Necesario para routerLink
    JwtModule.forRoot({
      config: {
        tokenGetter: tokenGetter,
        allowedDomains: ['localhost:5000'],
        disallowedRoutes: []
      }
    })
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: TokenInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }