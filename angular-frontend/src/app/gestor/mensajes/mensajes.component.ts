import { Component, OnInit } from '@angular/core';
import { ComunicacionService } from 'src/app/core/services/comunicacion.service';
import { UsuarioService } from 'src/app/core/services/usuario.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-mensajes',
  templateUrl: './mensajes.component.html',
  styleUrls: ['./mensajes.component.css']
})
export class MensajesComponent implements OnInit {
  // Variables para mensajes
  mensajesRecibidos: any[] = [];
  mensajesEnviados: any[] = [];

  // Estados
  cargandoRecibidos = true;
  cargandoEnviados = true;
  vistaActiva = 'recibidos'; // 'recibidos' o 'enviados'
  mostrarNuevoMensaje = false;

  // Estudiantes para enviar mensajes
  estudiantes: any[] = [];

  // Variables para el formulario de nuevo mensaje
  formularioMensaje: FormGroup;

  constructor(
    private comunicacionService: ComunicacionService,
    private usuarioService: UsuarioService,
    private fb: FormBuilder
  ) {
    this.formularioMensaje = this.fb.group({
      destinatario: ['', Validators.required],
      asunto: ['', Validators.required],
      contenido: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.cargarMensajesRecibidos();
    this.cargarMensajesEnviados();
    this.cargarEstudiantes();
  }

  cargarMensajesRecibidos(): void {
    this.cargandoRecibidos = true;
    this.comunicacionService.obtenerMensajesRecibidos().subscribe({
      next: (data) => {
        this.mensajesRecibidos = data;
        this.cargandoRecibidos = false;
      },
      error: (err) => {
        console.error('Error al cargar mensajes recibidos:', err);
        this.cargandoRecibidos = false;
      }
    });
  }

  cargarMensajesEnviados(): void {
    this.cargandoEnviados = true;
    this.comunicacionService.obtenerMensajesEnviados().subscribe({
      next: (data) => {
        this.mensajesEnviados = data;
        this.cargandoEnviados = false;
      },
      error: (err) => {
        console.error('Error al cargar mensajes enviados:', err);
        this.cargandoEnviados = false;
      }
    });
  }

  cargarEstudiantes(): void {
    this.usuarioService.getUsuarios().subscribe({
      next: (data) => {
        // Filtrar solo estudiantes
        this.estudiantes = data.filter((usuario: any) => usuario.id_rol === 3);
      },
      error: (err) => {
        console.error('Error al cargar estudiantes:', err);
      }
    });
  }

  cambiarVista(vista: string): void {
    this.vistaActiva = vista;
  }

  marcarComoLeido(idMensaje: number): void {
    this.comunicacionService.marcarComoLeido(idMensaje).subscribe({
      next: () => {
        // Actualizar el estado del mensaje en la lista
        const mensaje = this.mensajesRecibidos.find(m => m.id_mensaje === idMensaje);
        if (mensaje) {
          mensaje.leido = true;
        }
      },
      error: (err) => {
        console.error('Error al marcar como leído:', err);
      }
    });
  }

  toggleNuevoMensaje(): void {
    this.mostrarNuevoMensaje = !this.mostrarNuevoMensaje;
    // Resetear formulario al abrir
    if (this.mostrarNuevoMensaje) {
      this.formularioMensaje.reset();
    }
  }

  enviarMensaje(): void {
    if (this.formularioMensaje.invalid) {
      return;
    }

    const { destinatario, asunto, contenido } = this.formularioMensaje.value;

    this.comunicacionService.enviarMensaje(destinatario, asunto, contenido).subscribe({
      next: () => {
        // Recargar mensajes enviados y ocultar formulario
        this.cargarMensajesEnviados();
        this.mostrarNuevoMensaje = false;
        // Mostrar mensaje de éxito
        alert('Mensaje enviado con éxito');
      },
      error: (err) => {
        console.error('Error al enviar mensaje:', err);
        alert('Error al enviar mensaje: ' + err.message);
      }
    });
  }
}