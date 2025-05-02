import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-nueva-contrasena',
  templateUrl: './nueva-contrasena.component.html'
})
export class NuevaContrasenaComponent {
  correo = '';
  nueva = '';
  repetir = '';
  error = '';
  mensaje = '';

  constructor(private route: ActivatedRoute, private auth: AuthService, private router: Router) {
    this.route.queryParams.subscribe(params => {
      this.correo = params['correo'];
    });
  }

  cambiar() {
    if (this.nueva !== this.repetir) {
      this.error = 'Las contraseñas no coinciden';
      return;
    }

    this.auth.restablecerContrasena(this.correo, this.nueva).subscribe({
      next: () => {
        this.mensaje = 'Contraseña actualizada. Inicia sesión.';
        this.router.navigate(['/login']);
      },
      error: () => this.error = 'Error al actualizar la contraseña'
    });
  }
}
