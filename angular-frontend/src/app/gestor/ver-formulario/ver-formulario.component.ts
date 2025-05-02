import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormularioService } from 'src/app/core/services/formulario.service';

@Component({
  selector: 'app-ver-formulario',
  templateUrl: './ver-formulario.component.html',
  styleUrls: ['./ver-formulario.component.css']
})
export class VerFormularioComponent implements OnInit {
  formularios: any[] = [];
  formularioActual: any = null;
  idFormulario: number | null = null;
  
  // Estados de carga
  cargandoFormularios = true;
  cargandoDetalle = false;
  error = '';
  
  // Estado de vista
  modoLista = true;

  constructor(
    private formularioService: FormularioService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    // Verificar si se está solicitando un formulario específico
    this.route.params.subscribe(params => {
      if (params['id']) {
        this.idFormulario = +params['id'];
        this.modoLista = false;
        this.cargarDetalleFormulario(this.idFormulario);
      } else {
        this.modoLista = true;
        this.cargarFormularios();
      }
    });
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
        this.error = 'Error al cargar los formularios. Por favor, intenta nuevamente.';
        this.cargandoFormularios = false;
      }
    });
  }

  cargarDetalleFormulario(id: number): void {
    this.cargandoDetalle = true;
    this.formularioService.obtenerFormulario(id).subscribe({
      next: (data) => {
        this.formularioActual = data;
        this.cargandoDetalle = false;
      },
      error: (error) => {
        console.error(`Error al cargar el formulario con ID ${id}:`, error);
        this.error = 'Error al cargar el detalle del formulario. Por favor, intenta nuevamente.';
        this.cargandoDetalle = false;
      }
    });
  }

  verFormulario(id: number): void {
    this.router.navigate(['/gestor/formularios/ver', id]);
  }

  editarFormulario(id: number): void {
    this.router.navigate(['/gestor/formularios/editar', id]);
  }

  duplicarFormulario(id: number): void {
    this.cargandoDetalle = true;
    this.formularioService.obtenerFormulario(id).subscribe({
      next: (data) => {
        // Crear una copia del formulario
        const formularioDuplicado = { ...data };
        // Cambiar nombre para indicar que es una copia
        formularioDuplicado.nombre = `Copia de ${formularioDuplicado.nombre}`;
        // Eliminar ID para crear uno nuevo
        delete formularioDuplicado.id_formulario;
        delete formularioDuplicado.fecha_creacion;
        
        this.formularioService.crearFormulario(formularioDuplicado).subscribe({
          next: (response) => {
            this.cargarFormularios();
            this.cargandoDetalle = false;
          },
          error: (error) => {
            console.error('Error al duplicar el formulario:', error);
            this.error = 'Error al duplicar el formulario. Por favor, intenta nuevamente.';
            this.cargandoDetalle = false;
          }
        });
      },
      error: (error) => {
        console.error(`Error al obtener el formulario para duplicar:`, error);
        this.error = 'Error al duplicar el formulario. Por favor, intenta nuevamente.';
        this.cargandoDetalle = false;
      }
    });
  }

  eliminarFormulario(id: number): void {
    if (confirm('¿Estás seguro de que deseas eliminar este formulario? Esta acción no se puede deshacer.')) {
      this.formularioService.eliminarFormulario(id).subscribe({
        next: () => {
          // Si estamos viendo el detalle de este formulario, volver a la lista
          if (this.idFormulario === id) {
            this.router.navigate(['/gestor/formularios/ver']);
          } else {
            this.cargarFormularios();
          }
        },
        error: (error) => {
          console.error('Error al eliminar el formulario:', error);
          this.error = 'Error al eliminar el formulario. Por favor, intenta nuevamente.';
        }
      });
    }
  }

  cambiarEstadoFormulario(id: number, nuevoEstado: boolean): void {
    this.formularioService.cambiarEstado(id, nuevoEstado).subscribe({
      next: () => {
        // Actualizar estado en la lista local
        const formulario = this.formularios.find(f => f.id_formulario === id);
        if (formulario) {
          formulario.activo = nuevoEstado;
        }
        
        // Si estamos viendo el detalle, actualizar también allí
        if (this.formularioActual && this.formularioActual.id_formulario === id) {
          this.formularioActual.activo = nuevoEstado;
        }
      },
      error: (error) => {
        console.error('Error al cambiar el estado del formulario:', error);
        this.error = 'Error al cambiar el estado del formulario. Por favor, intenta nuevamente.';
      }
    });
  }

  volverALista(): void {
    this.router.navigate(['/gestor/formularios/ver']);
  }

  verMetricas(id: number): void {
    this.router.navigate(['/gestor/formularios/metricas', id]);
  }
}