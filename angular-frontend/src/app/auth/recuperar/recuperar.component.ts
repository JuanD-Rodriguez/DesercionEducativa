import { Component } from '@angular/core';
import { AuthService } from 'src/app/core/services/auth.service';

@Component({
  selector: 'app-recuperar',
  templateUrl: './recuperar.component.html'
})
export class RecuperarComponent {
  correo: string = '';
  mensaje: string = '';
  error: string = '';

  constructor(private authService: AuthService) {}

  enviarCodigo() {
    this.authService.enviarCodigo(this.correo).subscribe({
      next: () => {
        this.mensaje = 'Código enviado correctamente';
        this.error = '';
      },
      error: err => {
        this.error = err.error.message || 'Error al enviar el código';
        this.mensaje = '';
      }
    });
  }
}
