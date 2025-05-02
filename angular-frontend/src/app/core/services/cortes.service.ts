import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CortesService {
  private apiUrl = 'http://localhost:5000/api/cortes';

  constructor(private http: HttpClient) {}

  registrarCorte(corteData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/registrar`, corteData);
  }

  obtenerCortesEstudiante(idEstudiante: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/estudiante/${idEstudiante}`);
  }

  obtenerCortesCurso(idCurso: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/curso/${idCurso}`);
  }
}