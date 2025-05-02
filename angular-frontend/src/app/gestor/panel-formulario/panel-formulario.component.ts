import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormularioService } from 'src/app/core/services/formulario.service';

@Component({
  selector: 'app-panel-formulario',
  templateUrl: './panel-formulario.component.html',
  styleUrls: ['./panel-formulario.component.css']
})
export class PanelFormularioComponent implements OnInit {
  // Variables de datos
  nombreGestor = 'Gestor';
  formularios: any[] = [];
  cargandoFormularios = true;

  constructor(
    private formularioService: FormularioService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarDatosGestor();
    this.cargarFormularios();
  }

  cargarDatosGestor(): void {
    // Obtener datos del gestor desde el token JWT
    const token = localStorage.getItem('token');
    if (token) {
      try {
        // Aquí decodificarías el token para obtener el nombre del gestor
        const payload = JSON.parse(atob(token.split('.')[1]));
        this.nombreGestor = payload.nombre || 'Gestor';
      } catch (error) {
        console.error('Error al decodificar token:', error);
      }
    }
  }

  cargarFormularios(): void {
    this.cargandoFormularios = true;
    this.formularioService.obtenerFormularios().subscribe({
      next: (data) => {
        this.formularios = data;
        this.cargandoFormularios = false;
      },
      error: (error) => {
        console.error('Error al cargar formularios:', error);
        this.cargandoFormularios = false;
      }
    });
  }

  navigateToCrearEncuesta(): void {
    this.router.navigate(['/gestor/formularios/crear']);
  }

  navigateToVerEncuesta(): void {
    this.router.navigate(['/gestor/formularios/ver']);
  }

  navigateToVerMetricas(): void {
    this.router.navigate(['/gestor/formularios/metricas']);
  }
}