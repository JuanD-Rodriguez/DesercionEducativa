import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PrediccionService {
  private apiUrl = 'http://localhost:5000/api/prediccion';

  constructor(private http: HttpClient) {}

  predecirEstudiante(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/predecir/${id}`);
  }

  predecirGrupo(filtros: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/predecir_grupo`, filtros);
  }

  entrenarModelo(): Observable<any> {
    return this.http.post(`${this.apiUrl}/entrenar`, {});
  }
}