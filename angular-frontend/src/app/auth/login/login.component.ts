import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/core/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  nombre_usuario: string = '';
  contrasena: string = '';
  error: string = '';
  cargando: boolean = false;

  constructor(private authService: AuthService, private router: Router) {}

  iniciarSesion(): void {
    if (!this.nombre_usuario || !this.contrasena) {
      this.error = 'Por favor, complete todos los campos';
      return;
    }

    this.cargando = true;
    this.error = '';

    this.authService.login(this.nombre_usuario, this.contrasena).subscribe({
      next: (res: any) => {
        console.log('Login exitoso:', res);
        localStorage.setItem('token', res.access_token);
        
        try {
          // Decodificar el token para obtener el rol
          const tokenParts = res.access_token.split('.');
          if (tokenParts.length !== 3) {
            throw new Error('Formato de token inválido');
          }
          
          // Decodificar la parte del payload (segunda parte)
          const payload = JSON.parse(atob(tokenParts[1]));
          console.log('Payload completo del token:', payload);
          
          // Obtener información del usuario (del campo sub)
          if (payload.sub && typeof payload.sub === 'object') {
            const userInfo = payload.sub;
            console.log('Información de usuario:', userInfo);
            
            if (userInfo.hasOwnProperty('rol')) {
              const role = userInfo.rol;
              console.log('Rol del usuario:', role);
              
              // Usar navegación directa basada en el rol
              this.authService.navigateByRole();
            } else {
              console.error('No se encontró información de rol en el token');
              this.error = 'No se pudo determinar tu rol de usuario';
              this.cargando = false;
            }
          } else {
            console.error('No se encontró información de usuario en el token');
            this.error = 'No se pudo obtener la información de usuario';
            this.cargando = false;
          }
        } catch (error) {
          console.error('Error al procesar el token:', error);
          this.error = 'Error al procesar tu información de usuario';
          this.cargando = false;
        }
      },
      error: (err) => {
        console.error('Error de login:', err);
        this.error = err.error?.message || 'Credenciales inválidas';
        this.cargando = false;
      }
    });
  }
}