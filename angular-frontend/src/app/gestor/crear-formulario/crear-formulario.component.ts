// src/app/gestor/crear-formulario/crear-formulario.component.ts
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
  tiposDePregunta = ['texto', 'area_texto', 'opciones_multiple', 'opcion_unica'];

  constructor(
    private fb: FormBuilder,
    private formularioService: FormularioService,
    private router: Router
  ) {
    this.formularioForm = this.fb.group({
      titulo: ['', Validators.required],
      descripcion: [''],
      preguntas: this.fb.array([])
    });
  }

  ngOnInit(): void {
    this.agregarPregunta();
  }

  get preguntas() {
    return this.formularioForm.get('preguntas') as FormArray;
  }

  agregarPregunta() {
    this.preguntas.push(this.fb.group({
      texto: ['', Validators.required],
      tipo: ['texto', Validators.required],
      opciones: this.fb.array([])
    }));
  }

  eliminarPregunta(index: number) {
    this.preguntas.removeAt(index);
  }

  agregarOpcion(preguntaIndex: number) {
    const opciones = this.getOpciones(preguntaIndex);
    opciones.push(this.fb.control('', Validators.required));
  }

  eliminarOpcion(preguntaIndex: number, opcionIndex: number) {
    const opciones = this.getOpciones(preguntaIndex);
    opciones.removeAt(opcionIndex);
  }

  getOpciones(index: number): FormArray {
    return this.preguntas.at(index).get('opciones') as FormArray;
  }

  guardarFormulario() {
    if (this.formularioForm.valid) {
      const estructura_json = this.preguntas.value.map((preg: any) => ({
        texto: preg.texto,
        tipo: preg.tipo,
        opciones: preg.opciones || []
      }));

      const datos = {
        titulo: this.formularioForm.get('titulo')?.value,
        descripcion: this.formularioForm.get('descripcion')?.value,
        estructura_json
      };

      this.formularioService.crearFormulario(datos).subscribe({
        next: () => this.router.navigate(['/gestor/formularios']),
        error: err => console.error('Error al guardar formulario', err)
      });
    }
  }
}
