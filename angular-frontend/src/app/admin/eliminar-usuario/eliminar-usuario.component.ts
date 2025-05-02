import { Component, OnInit } from '@angular/core';
import { UsuarioService } from 'src/app/core/services/usuario.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-eliminar-usuario',
  templateUrl: './eliminar-usuario.component.html',
  styleUrls: ['./eliminar-usuario.component.css']
})
export class EliminarUsuarioComponent implements OnInit {
  usuarios: any[] = [];
  terminoBusqueda: string = '';
  busquedaRealizada: boolean = false;
  usuarioAEliminar: any = null;
  mensajeExito: string = '';
  mensajeError: string = '';

  constructor(
    private usuarioService: UsuarioService,
    private router: Router
  ) { }

  ngOnInit(): void {
    // Inicialmente podemos cargar todos los usuarios
    this.cargarUsuarios();
  }

  cargarUsuarios(): void {
    this.usuarioService.getUsuarios().subscribe({
      next: (data) => {
        console.log('Datos RAW de usuarios:', JSON.stringify(data, null, 2));
        
        // Procesar los usuarios para asegurar que tengan ID
        this.usuarios = (data as any[]).map(usuario => {
          // Asegurar que cada usuario tenga una propiedad id_usuario válida
          if (!usuario.id_usuario) {
            // Intentar obtener ID de diferentes propiedades
            usuario.id_usuario = usuario.id || usuario.id_estudiante || null;
            
            // Si hay algún ID numérico en el objeto, usarlo
            Object.keys(usuario).forEach(key => {
              if (key.includes('id') && typeof usuario[key] === 'number' && usuario[key] > 0 && !usuario.id_usuario) {
                console.log(`Encontrado ID alternativo en propiedad ${key}:`, usuario[key]);
                usuario.id_usuario = usuario[key];
              }
            });
          }
          return usuario;
        });
        
        this.busquedaRealizada = true;
        console.log('Usuarios procesados con IDs:', this.usuarios);
      },
      error: (error) => {
        console.error('Error al cargar usuarios:', error);
        this.mensajeError = 'Error al cargar la lista de usuarios. Por favor, intenta nuevamente.';
      }
    });
  }

  buscarUsuarios(): void {
    if (!this.terminoBusqueda.trim()) {
      this.cargarUsuarios();
      return;
    }

    const termino = this.terminoBusqueda.toLowerCase();
    this.usuarioService.getUsuarios().subscribe({
      next: (data) => {
        // Procesar los usuarios para asegurar que tengan ID
        const todosUsuarios = (data as any[]).map(usuario => {
          // Asegurar que cada usuario tenga una propiedad id_usuario válida
          if (!usuario.id_usuario) {
            usuario.id_usuario = usuario.id || usuario.id_estudiante || null;
            
            // Si hay algún ID numérico en el objeto, usarlo
            Object.keys(usuario).forEach(key => {
              if (key.includes('id') && typeof usuario[key] === 'number' && usuario[key] > 0 && !usuario.id_usuario) {
                usuario.id_usuario = usuario[key];
              }
            });
          }
          return usuario;
        });
        
        // Filtrar usuarios
        this.usuarios = todosUsuarios.filter(usuario => 
          (usuario.nombre?.toLowerCase().includes(termino) ||
           usuario.apellido?.toLowerCase().includes(termino) ||
           (usuario.correo_electronico || usuario.correo || '')?.toLowerCase().includes(termino) ||
           (usuario.id_usuario || usuario.id || '').toString().includes(termino))
        );
        
        this.busquedaRealizada = true;
        console.log('Resultados de búsqueda con IDs:', this.usuarios);
      },
      error: (error) => {
        console.error('Error en la búsqueda:', error);
        this.mensajeError = 'Error al realizar la búsqueda. Por favor, intenta nuevamente.';
      }
    });
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
    // Registro completo para depuración
    console.log('Usuario a eliminar (confirmarEliminar):', JSON.stringify(usuario, null, 2));
    
    // Verificar y establecer el ID si no existe
    if (!usuario.id_usuario && !usuario.id) {
      // Buscar alguna propiedad que contenga "id" y tenga un valor
      const posiblesIds = Object.entries(usuario)
        .filter(([key, value]) => key.toLowerCase().includes('id') && value);
      
      console.log('Posibles IDs encontrados:', posiblesIds);
      
      // Si hay propiedades de ID, usar la primera disponible
      if (posiblesIds.length > 0) {
        usuario.id_usuario = posiblesIds[0][1];
        console.log('Asignado ID alternativo:', usuario.id_usuario);
      }
    }
    
    this.usuarioAEliminar = usuario;
    // Limpiamos cualquier mensaje previo
    this.mensajeExito = '';
    this.mensajeError = '';
  }

  cancelarEliminar(): void {
    this.usuarioAEliminar = null;
  }

  eliminarUsuario(): void {
    if (!this.usuarioAEliminar) return;

    console.log('Eliminando usuario:', this.usuarioAEliminar);

    // Usar el ID disponible, ya sea id_usuario o id
    const idUsuario = this.usuarioAEliminar.id_usuario || this.usuarioAEliminar.id;
    
    // Si no hay un ID explícito, intentar buscar alguna propiedad con 'id'
    if (!idUsuario) {
      // Buscar alguna propiedad que contenga "id" y tenga un valor
      const posiblesIds = Object.entries(this.usuarioAEliminar)
        .filter(([key, value]) => key.toLowerCase().includes('id') && value && typeof value !== 'object');
      
      console.log('No se encontró ID directo. Posibles IDs alternativos:', posiblesIds);
      
      // Si hay propiedades de ID, usar la primera disponible
      if (posiblesIds.length > 0) {
        const id = posiblesIds[0][1];
        console.log('Usando ID alternativo para eliminar:', id);
        
        this.eliminarUsuarioConId(id);
        return;
      } else {
        this.mensajeError = 'No se puede eliminar el usuario porque no tiene ID.';
        this.usuarioAEliminar = null;
        return;
      }
    }
    
    this.eliminarUsuarioConId(idUsuario);
  }
  
  eliminarUsuarioConId(id: any): void {
    console.log('Ejecutando eliminación con ID:', id);
    
    this.usuarioService.eliminarUsuario(id).subscribe({
      next: () => {
        this.mensajeExito = `El usuario ${this.usuarioAEliminar.nombre} ha sido eliminado correctamente.`;
        this.usuarios = this.usuarios.filter(u => {
          const userId = u.id_usuario || u.id;
          return userId !== id;
        });
        this.usuarioAEliminar = null;
        
        // Si ya no quedan usuarios en la lista después de filtrar, actualizar la bandera
        if (this.usuarios.length === 0) {
          this.busquedaRealizada = true;
        }
      },
      error: (error) => {
        console.error('Error al eliminar usuario:', error);
        this.mensajeError = 'Error al eliminar el usuario. Por favor, intenta nuevamente.';
        this.usuarioAEliminar = null;
      }
    });
  }
}