import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UsuarioService } from 'src/app/core/services/usuario.service';

@Component({
  selector: 'app-editar-usuario',
  templateUrl: './editar-usuario.component.html',
  styleUrls: ['./editar-usuario.component.css']
})
export class EditarUsuarioComponent implements OnInit {
  usuarioId: number = 0;
  usuarioForm!: FormGroup;
  cargando: boolean = false;
  errorMensaje: string = '';
  exitoMensaje: string = '';
  datosOriginales: any = {};

  terminoBusqueda: string = '';
  resultadosBusqueda: any[] = [];
  busquedaRealizada: boolean = false;

  constructor(
    private fb: FormBuilder,
    private usuarioService: UsuarioService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.usuarioForm = this.fb.group({
      nombre: ['', Validators.required],
      apellidos: ['', Validators.required],
      correo: ['', [Validators.required, Validators.email]],
      telefono: ['', [Validators.required, Validators.pattern(/^[0-9]{10}$/)]],
      id_ingenieria: ['', Validators.required],
      rol_id: [3, Validators.required]
    });

    this.route.params.subscribe(params => {
      const id = +params['id'];
      if (id && id > 0) {
        this.usuarioId = id;
        this.cargarDatosUsuario();
      }
    });
  }

  buscarUsuarios(): void {
    if (!this.terminoBusqueda.trim()) {
      this.resultadosBusqueda = [];
      this.busquedaRealizada = false;
      return;
    }

    this.cargando = true;
    const termino = this.terminoBusqueda.toLowerCase();

    this.usuarioService.getUsuarios().subscribe({
      next: (usuarios) => {
        this.resultadosBusqueda = usuarios
          .filter((usuario: any) => 
            (usuario.nombre?.toLowerCase().includes(termino) ||
             (usuario.apellido || '')?.toLowerCase().includes(termino) ||
             (usuario.correo_electronico || usuario.correo || '')?.toLowerCase().includes(termino) ||
             (usuario.id_usuario || usuario.id)?.toString().includes(termino))
          )
          .map((usuario: any) => {
            if (!usuario.id_usuario && usuario.id) {
              usuario.id_usuario = usuario.id;
            }
            return usuario;
          });

        this.busquedaRealizada = true;
        this.cargando = false;
        console.log('Resultados de búsqueda:', this.resultadosBusqueda);
      },
      error: (error) => {
        console.error('Error al buscar usuarios:', error);
        this.errorMensaje = 'Error al buscar usuarios. Por favor, intenta nuevamente.';
        this.cargando = false;
        this.busquedaRealizada = true;
      }
    });
  }

  seleccionarUsuario(id: number): void {
    console.log('Usuario seleccionado con ID:', id);

    if (!id) {
      this.errorMensaje = 'ID de usuario no válido';
      return;
    }

    this.usuarioId = id;
    this.cargarDatosUsuario();
  }

  cargarDatosUsuario(): void {
    this.cargando = true;
    console.log('Cargando datos del usuario con ID:', this.usuarioId);

    this.usuarioService.getUsuario(this.usuarioId).subscribe({
      next: (usuario: any) => {
        this.datosOriginales = usuario;
        console.log('Datos de usuario recibidos:', usuario);

        this.usuarioForm.patchValue({
          nombre: usuario.nombre || '',
          apellidos: usuario.apellido || '',
          correo: usuario.correo_electronico || usuario.correo || '',
          telefono: usuario.telefono || '',
          id_ingenieria: usuario.id_ingenieria || '',
          rol_id: usuario.rol_id || usuario.id_rol || 3
        });
        this.cargando = false;
      },
      error: (error) => {
        console.error('Error al cargar datos del usuario:', error);
        this.errorMensaje = 'Error al cargar datos del usuario. Intente nuevamente.';
        this.cargando = false;
      }
    });
  }

  onSubmit(): void {
    if (this.usuarioForm.invalid) {
      this.usuarioForm.markAllAsTouched();
      return;
    }
  
    // Estructurar los datos según lo que espera el backend
    const datosActualizados = {
      id_rol: this.usuarioForm.value.rol_id,
    };
  
    // Agregar datos específicos según el rol
    if (this.usuarioForm.value.rol_id == 3) {  // Estudiante
      datosActualizados['estudiante'] = {
        nombre: this.usuarioForm.value.nombre,
        apellido: this.usuarioForm.value.apellidos,
        correo_electronico: this.usuarioForm.value.correo,
        id_ingenieria: this.usuarioForm.value.id_ingenieria
      };
    } else if (this.usuarioForm.value.rol_id == 2) {  // Gestor
      datosActualizados['gestor'] = {
        nombre: this.usuarioForm.value.nombre,
        apellido: this.usuarioForm.value.apellidos,
        telefono: this.usuarioForm.value.telefono
      };
    }
  
    // Si hay contraseña, incluirla
    if (this.datosOriginales.contrasena) {
      datosActualizados['contrasena'] = this.datosOriginales.contrasena;
    }
  
    console.log('Enviando actualización para usuario ID:', this.usuarioId);
    console.log('Datos de actualización:', datosActualizados);
  
    this.cargando = true;
    this.usuarioService.actualizarUsuario(this.usuarioId, datosActualizados).subscribe({
      next: () => {
        this.exitoMensaje = 'Usuario actualizado exitosamente';
        this.errorMensaje = '';
        this.cargando = false;
        
        // Redireccionar después de un breve retraso
        setTimeout(() => {
          this.router.navigate(['/admin/usuarios']);
        }, 2000);
      },
      error: (error) => {
        console.error('Error al actualizar usuario:', error);
        this.errorMensaje = 'Error al actualizar el usuario. Intente nuevamente.';
        this.exitoMensaje = '';
        this.cargando = false;
      }
    });
  }

  cancelar(): void {
    this.router.navigate(['/admin/usuarios']);
  }
}