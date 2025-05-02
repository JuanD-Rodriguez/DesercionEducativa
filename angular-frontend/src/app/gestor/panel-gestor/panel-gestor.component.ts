import { Component, OnInit } from '@angular/core';
import { ReportesService } from 'src/app/core/services/reportes.service';
import { ComunicacionService } from 'src/app/core/services/comunicacion.service';
import { AuthService } from 'src/app/core/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-panel-gestor',
  templateUrl: './panel-gestor.component.html',
  styleUrls: ['./panel-gestor.component.css']
})
export class PanelGestorComponent implements OnInit {
  // Variables de datos
  nombreGestor = 'Gestor';
  estadisticas: any = {};
  estudiantesRiesgo: any[] = [];
  mensajesNoLeidos = 0;

  // Estados de carga
  cargandoEstadisticas = true;
  cargandoEstudiantes = true;
  cargandoMensajes = true;

  constructor(
    private reportesService: ReportesService,
    private comunicacionService: ComunicacionService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarDatosGestor();
    this.cargarEstadisticas();
    this.cargarEstudiantesRiesgo();
    this.cargarMensajesNoLeidos();
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

  cargarEstadisticas(): void {
    this.cargandoEstadisticas = true;
    this.reportesService.obtenerEstadisticasGenerales().subscribe({
      next: (data) => {
        this.estadisticas = data;
        this.cargandoEstadisticas = false;
      },
      error: (error) => {
        console.error('Error al cargar estadísticas:', error);
        this.cargandoEstadisticas = false;
      }
    });
  }

  cargarEstudiantesRiesgo(): void {
    this.cargandoEstudiantes = true;
    this.reportesService.obtenerEstudiantesAltoRiesgo(0.7).subscribe({
      next: (data) => {
        // Solo mostrar los primeros 5 estudiantes en el dashboard
        this.estudiantesRiesgo = data.slice(0, 5);
        this.cargandoEstudiantes = false;
      },
      error: (error) => {
        console.error('Error al cargar estudiantes en riesgo:', error);
        this.cargandoEstudiantes = false;
      }
    });
  }

  cargarMensajesNoLeidos(): void {
    this.cargandoMensajes = true;
    this.comunicacionService.obtenerMensajesRecibidos().subscribe({
      next: (mensajes) => {
        // Contar mensajes no leídos
        this.mensajesNoLeidos = mensajes.filter(m => !m.leido).length;
        this.cargandoMensajes = false;
      },
      error: (error) => {
        console.error('Error al cargar mensajes:', error);
        this.cargandoMensajes = false;
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}