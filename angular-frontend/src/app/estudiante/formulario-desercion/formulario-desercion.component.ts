import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { FormularioService } from 'src/app/core/services/formulario.service';

@Component({
  selector: 'app-formulario-desercion',
  templateUrl: './formulario-desercion.component.html',
  styleUrls: ['./formulario-desercion.component.css']
})
export class FormularioDesercionComponent implements OnInit {
  formulario: FormGroup;
  preguntas: any[] = [];
  enviado: boolean = false;
  idFormulario: number = 0;

  constructor(
    private fb: FormBuilder,
    private formularioService: FormularioService,
    private route: ActivatedRoute
  ) {
    this.formulario = this.fb.group({
      respuestas: this.fb.array([])
    });
  }

  get respuestas(): FormArray {
    return this.formulario.get('respuestas') as FormArray;
  }

  ngOnInit(): void {
    this.idFormulario = Number(this.route.snapshot.paramMap.get('id'));
    this.formularioService.getPreguntas(this.idFormulario).subscribe(preguntas => {
      this.preguntas = preguntas;
      preguntas.forEach(p => {
        this.respuestas.push(this.fb.group({
          texto: [p.texto],
          respuesta: ['', Validators.required]
        }));
      });
    });
  }

  enviarFormulario(): void {
    const respuestasFormateadas = this.respuestas.value.map((r: any) => ({
      texto: r.texto,
      respuesta: r.respuesta
    }));

    this.formularioService.enviarRespuestas(this.idFormulario, respuestasFormateadas).subscribe(() => {
      this.enviado = true;
    });
  }

  volver(): void {
    window.location.href = '/estudiante';
  }
}
