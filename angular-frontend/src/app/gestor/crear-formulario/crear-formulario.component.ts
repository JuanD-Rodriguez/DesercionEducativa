import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { FormularioService } from 'src/app/core/services/formulario.service';

@Component({
  selector: 'app-crear-formulario',
  templateUrl: './crear-formulario.component.html',
  styleUrls: ['./crear-formulario.component.css']
})
export class CrearFormularioComponent implements OnInit {
  formularioForm: FormGroup;
  tiposDePregunta = [
    { id: 'texto', nombre: 'Campo de texto' },
    { id: 'opciones_multiple', nombre: 'Selector de opciones múltiples' },
    { id: 'opcion', nombre: 'Botones de opción' },
    { id: 'opcion_unica', nombre: 'Selector opción única' },
    { id: 'area_texto', nombre: 'Área de texto' },
    { id: 'desplegable', nombre: 'Selector desplegable' }
  ];
  
  enviando = false;
  exito = false;
  error = '';

  constructor(
    private fb: FormBuilder,
    private formularioService: FormularioService,
    private router: Router
  ) {
    this.formularioForm = this.fb.group({
      nombre: ['Formulario de Deserción', Validators.required],
      descripcion: ['Encuesta para identificar factores de deserción'],
      activo: [true],
      preguntas: this.fb.array([])
    });
  }

  ngOnInit(): void {
    // Añadir preguntas por defecto
    this.agregarPregunta();
  }

  get preguntas() {
    return this.formularioForm.get('preguntas') as FormArray;
  }

  agregarPregunta() {
    const preguntaGroup = this.fb.group({
      textoPregunta: ['', Validators.required],
      tipoPregunta: ['texto', Validators.required],
      obligatoria: [true],
      categoria: ['academico'], // Por defecto, categoría académica
      opciones: this.fb.array([])
    });
    
    this.preguntas.push(preguntaGroup);
    
    // Si es un tipo de pregunta que necesita opciones, añadimos algunas por defecto
    if (['opciones_multiple', 'opcion', 'opcion_unica', 'desplegable'].includes(preguntaGroup.get('tipoPregunta')?.value)) {
      this.agregarOpcion(this.preguntas.length - 1);
      this.agregarOpcion(this.preguntas.length - 1);
    }
  }

  eliminarPregunta(index: number) {
    this.preguntas.removeAt(index);
  }

  getOpciones(preguntaIndex: number) {
    return (this.preguntas.at(preguntaIndex).get('opciones') as FormArray);
  }

  agregarOpcion(preguntaIndex: number) {
    const opcionesArray = this.preguntas.at(preguntaIndex).get('opciones') as FormArray;
    opcionesArray.push(this.fb.group({
      textoOpcion: ['', Validators.required],
      valor: ['']
    }));
  }

  eliminarOpcion(preguntaIndex: number, opcionIndex: number) {
    const opcionesArray = this.preguntas.at(preguntaIndex).get('opciones') as FormArray;
    opcionesArray.removeAt(opcionIndex);
  }

  cambioTipoPregunta(preguntaIndex: number) {
    const pregunta = this.preguntas.at(preguntaIndex);
    const tipoPregunta = pregunta.get('tipoPregunta')?.value;
    const opcionesArray = pregunta.get('opciones') as FormArray;
    
    // Limpiar opciones existentes
    while (opcionesArray.length > 0) {
      opcionesArray.removeAt(0);
    }
    
    // Añadir opciones por defecto para tipos que las necesitan
    if (['opciones_multiple', 'opcion', 'opcion_unica', 'desplegable'].includes(tipoPregunta)) {
      this.agregarOpcion(preguntaIndex);
      this.agregarOpcion(preguntaIndex);
    }
  }
  guardarFormulario() {
    if (this.formularioForm.valid) {
      this.enviando = true;
      this.error = '';
      
      console.log('Formulario a enviar:', this.formularioForm.value);
      
      this.formularioService.crearFormulario(this.formularioForm.value)
        .subscribe({
          next: (response) => {
            console.log('Respuesta del servidor:', response);
            this.enviando = false;
            this.exito = true;
            
            // Navegar a la página de formularios después de 2 segundos
            setTimeout(() => {
              this.router.navigate(['/gestor/formularios']);
            }, 2000);
          },
          error: (error) => {
            console.error('Error completo:', error);
            this.enviando = false;
            this.error = `Error al guardar el formulario: ${error.error?.error || error.message || 'Error desconocido'}`;
          }
        });
    } else {
      this.error = 'Por favor, completa todos los campos obligatorios.';
      this.marcarFormularioComoTouched(this.formularioForm);
    }
  }
  marcarFormularioComoTouched(formGroup: FormGroup) {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      
      if (control instanceof FormGroup) {
        this.marcarFormularioComoTouched(control);
      } else if (control instanceof FormArray) {
        for (let i = 0; i < control.length; i++) {
          if (control.at(i) instanceof FormGroup) {
            this.marcarFormularioComoTouched(control.at(i) as FormGroup);
          } else {
            control.at(i).markAsTouched();
          }
        }
      } else {
        control?.markAsTouched();
      }
    });
  }

  cancelar() {
    this.router.navigate(['/gestor/formularios']);
  }
}