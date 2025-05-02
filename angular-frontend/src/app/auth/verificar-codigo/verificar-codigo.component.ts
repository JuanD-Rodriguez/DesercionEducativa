import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from 'src/app/core/services/auth.service';

@Component({
  selector: 'app-verificar-codigo',
  templateUrl: './verificar-codigo.component.html',
  styleUrls: ['./verificar-codigo.component.css']
})
export class VerificarCodigoComponent implements OnInit {
  correo: string = '';
  codigo: string = '';
  error: string = '';
  codigoVerificado: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
    // Obtener el correo de los parámetros de consulta
    this.route.queryParams.subscribe(params => {
      this.correo = params['correo'];
      
      if (!this.correo) {
        this.error = 'No se proporcionó un correo electrónico válido.';
        // Redirigir a la página de recuperación si no hay correo
        setTimeout(() => {
          this.router.navigate(['/recuperar']);
        }, 2000);
      }
    });
  }

  verificarCodigo(): void {
    if (!this.codigo) {
      this.error = 'Por favor, ingresa el código de verificación.';
      return;
    }

    this.authService.verificarCodigo(this.correo, this.codigo).subscribe({
      next: () => {
        this.codigoVerificado = true;
        this.error = '';
      },
      error: (err) => {
        this.error = err.error?.message || 'El código ingresado no es válido. Inténtalo nuevamente.';
      }
    });
  }

  irANuevaContrasena(): void {
    this.router.navigate(['/nueva-contrasena'], { 
      queryParams: { correo: this.correo } 
    });
  }
}