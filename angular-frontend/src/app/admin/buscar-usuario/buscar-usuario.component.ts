import { Component, OnInit } from '@angular/core';
import { UsuarioService } from 'src/app/core/services/usuario.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-buscar-usuario',
  templateUrl: './buscar-usuario.component.html',
  styleUrls: ['./buscar-usuario.component.css']
})
export class BuscarUsuarioComponent implements OnInit {
  terminoBusqueda: string = '';
  filtroTipo: string = 'todos';
  resultados: any[] = [];
  busquedaRealizada: boolean = false;
  cargando: boolean = false;
  usuarioAEliminar: any = null;

  constructor(private usuarioService: UsuarioService, private router: Router) { }

  ngOnInit(): void {
    // Inicialización
  }

  buscarUsuarios(): void {
    // Implementación
    this.cargando = true;
    this.usuarioService.getUsuarios().subscribe({
      next: (usuarios) => {
        // Asegurarnos de que todos los usuarios tengan un ID
        const usuariosProcessed = (usuarios as any[]).map(usuario => {
          this.asegurarIdUsuario(usuario);
          return usuario;
        });
        
        console.log('Usuarios procesados con IDs:', usuariosProcessed);
        
        if (!this.terminoBusqueda.trim()) {
          this.resultados = usuariosProcessed;
        } else {
          const termino = this.terminoBusqueda.toLowerCase();
          this.resultados = usuariosProcessed.filter(u => 
            (u.nombre?.toLowerCase().includes(termino) || 
             (u.apellido || '')?.toLowerCase().includes(termino) ||
             (u.correo_electronico || u.correo || '')?.toLowerCase().includes(termino))
          );
        }
        
        this.busquedaRealizada = true;
        this.cargando = false;
        this.aplicarFiltros();
        console.log('Resultados de búsqueda:', this.resultados);
      },
      error: (error) => {
        console.error('Error al buscar usuarios:', error);
        this.cargando = false;
        this.busquedaRealizada = true;
      }
    });
  }

  // Método para asegurar que todos los usuarios tengan un ID válido
  private asegurarIdUsuario(usuario: any): void {
    if (!usuario.id_usuario && !usuario.id) {
      // Buscar propiedades que podrían contener IDs
      for (const key in usuario) {
        if (key.toLowerCase().includes('id') && 
            typeof usuario[key] === 'number' && 
            usuario[key] > 0 &&
            key !== 'id_rol' &&
            key !== 'rol_id') {
          usuario.id_usuario = usuario[key];
          console.log(`Asignado ID alternativo desde ${key}:`, usuario.id_usuario);
          break;
        }
      }
      
      // Si sigue sin ID, asignar un ID temporal
      if (!usuario.id_usuario && !usuario.id) {
        if (usuario.id_estudiante) {
          usuario.id_usuario = usuario.id_estudiante;
        } else if (usuario.id_gestor) {
          usuario.id_usuario = usuario.id_gestor;
        }
      }
    } else if (!usuario.id_usuario && usuario.id) {
      usuario.id_usuario = usuario.id;
    }
  }

  aplicarFiltros(): void {
    if (this.filtroTipo === 'todos') {
      return;
    }
    
    let rolId: number;
    switch (this.filtroTipo) {
      case 'admin':
        rolId = 1;
        break;
      case 'gestor':
        rolId = 2;
        break;
      case 'estudiante':
        rolId = 3;
        break;
      default:
        return;
    }
    
    this.resultados = this.resultados.filter(u => 
      (u.id_rol || u.rol_id) === rolId
    );
  }

  getTipoUsuario(id_rol: number): string {
    switch (id_rol) {
      case 1:
        return 'Administrador';
      case 2:
        return 'Gestor';
      case 3:
        return 'Estudiante';
      default:
        return 'Desconocido';
    }
  }

  confirmarEliminar(usuario: any): void {
    // Asegurarnos de que el usuario tenga un ID antes de confirmarlo
    this.asegurarIdUsuario(usuario);
    
    // Logging para depuración
    console.log('Usuario a eliminar:', usuario);
    console.log('ID del usuario a eliminar:', usuario.id_usuario || usuario.id);
    
    // Verificar explícitamente si tiene ID
    if (!usuario.id_usuario && !usuario.id) {
      alert('No se puede eliminar el usuario porque no tiene ID.');
      return;
    }
    
    this.usuarioAEliminar = usuario;
  }

  cancelarEliminar(): void {
    this.usuarioAEliminar = null;
  }

  eliminarUsuario(): void {
    if (!this.usuarioAEliminar) return;
    
    // Obtener ID y verificar nuevamente
    const id = this.usuarioAEliminar.id_usuario || this.usuarioAEliminar.id;
    console.log('Eliminando usuario con ID:', id);
    
    if (!id) {
      alert('No se puede eliminar el usuario porque no tiene ID.');
      this.usuarioAEliminar = null;
      return;
    }
    
    this.usuarioService.eliminarUsuario(id).subscribe({
      next: () => {
        // Actualizar la lista de resultados eliminando el usuario
        this.resultados = this.resultados.filter(u => 
          (u.id_usuario || u.id) !== id
        );
        
        this.usuarioAEliminar = null;
        alert('Usuario eliminado con éxito');
      },
      error: (error) => {
        console.error('Error eliminando usuario:', error);
        this.usuarioAEliminar = null;
        alert('Error al eliminar el usuario: ' + (error.message || 'Error desconocido'));
      }
    });
  }
}