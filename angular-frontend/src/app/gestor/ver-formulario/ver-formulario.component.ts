// src/app/gestor/ver-formulario/ver-formulario.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormularioService } from 'src/app/core/services/formulario.service';

@Component({
  selector: 'app-ver-formulario',
  templateUrl: './ver-formulario.component.html',
  styleUrls: ['./ver-formulario.component.css']
})
export class VerFormularioComponent implements OnInit {
  id: number = 0;
  formularioActual: any;
  formularios: any[] = [];
  modoLista: boolean = true;
  error: string = '';
  cargandoFormularios: boolean = false;
  cargandoDetalle: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private formularioService: FormularioService
  ) {}

  ngOnInit(): void {
    this.id = Number(this.route.snapshot.paramMap.get('id'));
    if (this.id) {
      this.modoLista = false;
      this.cargarDetalleFormulario();
    } else {
      this.cargarFormularios();
    }
  }

  cargarFormularios(): void {
    this.cargandoFormularios = true;
    this.formularioService.obtenerFormularios().subscribe({
      next: data => {
        this.formularios = data;
        this.cargandoFormularios = false;
      },
      error: err => {
        this.error = 'Error al cargar formularios';
        this.cargandoFormularios = false;
      }
    });
  }

  cargarDetalleFormulario(): void {
    this.cargandoDetalle = true;
    this.formularioService.obtenerFormulario(this.id).subscribe({
      next: data => {
        this.formularioActual = data;
        this.cargandoDetalle = false;
      },
      error: err => {
        this.error = 'No se pudo cargar el formulario';
        this.cargandoDetalle = false;
      }
    });
  }

  verFormulario(id: number): void {
    this.id = id;
    this.modoLista = false;
    this.cargarDetalleFormulario();
  }

  volverALista(): void {
    this.modoLista = true;
    this.id = 0;
    this.formularioActual = null;
    this.cargarFormularios();
  }

  editarFormulario(id: number): void {
    // Lógica de navegación a la edición
    console.log('Editar formulario', id);
  }

  verMetricas(id: number): void {
    // Lógica de navegación a métricas
    console.log('Ver métricas del formulario', id);
  }

  duplicarFormulario(id: number): void {
    console.log('Duplicar formulario', id);
  }

  cambiarEstadoFormulario(id: number, nuevoEstado: boolean): void {
    const estadoStr = nuevoEstado ? 'activo' : 'inactivo';
    this.formularioService.cambiarEstado(id, estadoStr).subscribe({
      next: () => this.cargarFormularios(),
      error: () => this.error = 'No se pudo cambiar el estado'
    });
  }

  eliminarFormulario(id: number): void {
    this.formularioService.eliminarFormulario(id).subscribe({
      next: () => this.cargarFormularios(),
      error: () => this.error = 'No se pudo eliminar el formulario'
    });
  }
}
