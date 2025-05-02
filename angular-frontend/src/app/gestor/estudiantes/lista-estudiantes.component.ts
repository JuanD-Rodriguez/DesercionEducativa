import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UsuarioService } from 'src/app/core/services/usuario.service';
import { AuthService } from 'src/app/core/services/auth.service';
import { ComunicacionService } from 'src/app/core/services/comunicacion.service';

@Component({
  selector: 'app-lista-estudiantes',
  templateUrl: './lista-estudiantes.component.html',
  styleUrls: ['./lista-estudiantes.component.css']
})
export class ListaEstudiantesComponent implements OnInit {
  estudiantes: any[] = [];
  filtroNombre: string = '';
  cargando: boolean = true;
  errores: string[] = [];
  mensajesNoLeidos: number = 0;

  // Paleta de colores para las iniciales
  colores: string[] = [
    '#C8A2C8', // Lavender
    '#B5D3E7', // Light Blue
    '#FFD1DC', // Light Pink
    '#B0E0E6', // Powder Blue
    '#FFDAB9', // Peach
    '#E6E6FA', // Lavender (lighter)
    '#D8BFD8', // Thistle
    '#F0E68C', // Khaki
    '#D3D3D3', // Light Grey
    '#A0DAA9'  // Light Green
  ];

  constructor(
    private router: Router,
    private usuarioService: UsuarioService,
    private authService: AuthService,
    private comunicacionService: ComunicacionService
  ) {}

  ngOnInit(): void {
    this.cargarEstudiantes();
    this.cargarMensajesNoLeidos();
  }

  cargarEstudiantes(): void {
    this.cargando = true;
    this.errores = []; // Limpiar errores previos
    
    this.usuarioService.getUsuarios().subscribe({
      next: (data) => {
        console.log('Datos de estudiantes recibidos:', data);
        this.estudiantes = data;
        this.cargando = false;
      },
      error: (err) => {
        console.error('Error al cargar estudiantes:', err);
        this.errores.push('Error al cargar la lista de estudiantes: ' + err.message);
        this.cargando = false;
      }
    });
  }

  cargarMensajesNoLeidos(): void {
    this.comunicacionService.obtenerMensajesRecibidos().subscribe({
      next: (mensajes) => {
        // Contar mensajes no leídos
        this.mensajesNoLeidos = mensajes.filter(m => !m.leido).length;
      },
      error: (error) => {
        console.error('Error al cargar mensajes:', error);
      }
    });
  }

  filtrarEstudiantes(): any[] {
    if (!this.filtroNombre.trim()) {
      return this.estudiantes;
    }
    
    const filtro = this.filtroNombre.toLowerCase();
    return this.estudiantes.filter(est => 
      (est.nombre?.toLowerCase().includes(filtro) || 
       est.apellido?.toLowerCase().includes(filtro))
    );
  }

  // Método para obtener un color consistente para cada letra
  getColorForLetra(letra: string): string {
    const letraNormalizada = letra.toUpperCase();
    const codigo = letraNormalizada.charCodeAt(0);
    const index = (codigo - 65) % this.colores.length;
    return this.colores[Math.max(0, index)]; // Protección contra caracteres no alfabéticos
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}