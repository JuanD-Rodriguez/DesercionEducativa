
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray } from '@angular/forms';
import { FormularioService } from 'src/app/core/services/formulario.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-formulario-desercion',
  templateUrl: './formulario-desercion.component.html'
})
export class FormularioDesercionComponent implements OnInit {
  formulario: FormGroup;
  enviado = false;

  constructor(private fb: FormBuilder, private formularioService: FormularioService, private router: Router) {
    this.formulario = this.fb.group({
      respuestas: this.fb.array([])  // array de respuestas a preguntas
    });
  }

  ngOnInit(): void {
    this.cargarPreguntas();
  }

  get respuestas(): FormArray {
    return this.formulario.get('respuestas') as FormArray;
  }

  cargarPreguntas() {
    this.formularioService.getPreguntas().subscribe(preguntas => {
      preguntas.forEach((preg: any) => {
        this.respuestas.push(this.fb.group({
          id_pregunta: [preg.ID_Pregunta],
          texto: [preg.Texto_Pregunta],
          respuesta: ['', Validators.required]
        }));
      });
    });
  }

  enviarFormulario() {
    if (this.formulario.valid) {
      const respuestasFormateadas = this.respuestas.value.map((r: any) => ({
        id_pregunta: r.id_pregunta,
        opcion_seleccionada: r.respuesta
      }));

      this.formularioService.enviarRespuestas(respuestasFormateadas).subscribe(() => {
        this.enviado = true;
        this.router.navigate(['/']);
      });
    }
  }
}
