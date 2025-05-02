import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UsuarioService } from 'src/app/core/services/usuario.service';
import { Router } from '@angular/router';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-crear-usuario',
  templateUrl: './crear-usuario.component.html',
  styleUrls: ['./crear-usuario.component.css']
})
export class CrearUsuarioComponent implements OnInit {
  usuarioForm!: FormGroup;
  enviando = false;
  errorMessage = '';
  ingenierias: any[] = [];
  cargandoIngenierias = false;

  constructor(
    private fb: FormBuilder,
    private usuarioService: UsuarioService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.inicializarFormulario();
    this.cargarIngenierias();
  }

  inicializarFormulario(): void {
    this.usuarioForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      apellidos: ['', [Validators.required, Validators.minLength(2)]],
      correo: ['', [Validators.required, Validators.email, Validators.pattern(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/)]],
      telefono: ['', [Validators.required, Validators.pattern(/^[0-9]{10}$/)]],
      id_ingenieria: ['', Validators.required],
      contrasena: ['', [Validators.required, Validators.minLength(8)]],
      fecha_registro: [new Date().toISOString().split('T')[0], Validators.required]
    });
  }

  cargarIngenierias(): void {
    this.cargandoIngenierias = true;
    this.usuarioService.obtenerIngenierias()
      .pipe(finalize(() => this.cargandoIngenierias = false))
      .subscribe({
        next: (data) => {
          this.ingenierias = data;
          console.log('Ingenierías cargadas:', this.ingenierias);
        },
        error: (err) => {
          console.error('Error al cargar ingenierías:', err);
          // Usar lista de ingenierías de respaldo
          this.ingenierias = [
            { id_ingenieria: 1, nombre_ingenieria: 'Ingeniería de Sistemas' },
            { id_ingenieria: 2, nombre_ingenieria: 'Ingeniería Electrónica' },
            { id_ingenieria: 3, nombre_ingenieria: 'Ingeniería Mecánica' },
            { id_ingenieria: 4, nombre_ingenieria: 'Ingeniería Industrial' },
            { id_ingenieria: 5, nombre_ingenieria: 'Ingeniería Ambiental' }
          ];
        }
      });
  }

  onSubmit(): void {
    if (this.usuarioForm.invalid) {
      this.usuarioForm.markAllAsTouched();
      return;
    }
    
    this.enviando = true;
    this.errorMessage = '';
  
    const datosUsuario = {
      nombre: this.usuarioForm.value.nombre,
      apellido: this.usuarioForm.value.apellidos,
      correo: this.usuarioForm.value.correo,
      correo_electronico: this.usuarioForm.value.correo,
      telefono: this.usuarioForm.value.telefono,
      id_ingenieria: this.usuarioForm.value.id_ingenieria,
      contrasena: this.usuarioForm.value.contrasena,
      fecha_registro: this.usuarioForm.value.fecha_registro
    };
  
    this.usuarioService.crearUsuario(datosUsuario)
      .pipe(finalize(() => this.enviando = false))
      .subscribe({
        next: (respuesta) => {
          console.log('Respuesta del servidor:', respuesta);
          this.mostrarMensaje('Usuario registrado exitosamente');
          this.router.navigate(['/admin/usuarios']);
        },
        error: (err) => {
          console.error('Error al crear usuario:', err);
          this.errorMessage = 'Error al crear usuario: ' + err.message;
          this.mostrarMensaje(this.errorMessage);
        }
      });
  }

  mostrarMensaje(mensaje: string): void {
    alert(mensaje);
  }

  // Getters para acceder fácilmente a los controles del formulario en la plantilla
  get nombreControl() { return this.usuarioForm.get('nombre'); }
  get apellidosControl() { return this.usuarioForm.get('apellidos'); }
  get correoControl() { return this.usuarioForm.get('correo'); }
  get telefonoControl() { return this.usuarioForm.get('telefono'); }
  get ingenieriaControl() { return this.usuarioForm.get('id_ingenieria'); }
  get contrasenaControl() { return this.usuarioForm.get('contrasena'); }
}