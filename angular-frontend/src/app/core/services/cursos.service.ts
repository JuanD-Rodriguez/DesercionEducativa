import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CursosService {
  private apiUrl = 'http://localhost:5000/api/cursos';

  constructor(private http: HttpClient) {}

  obtenerCursos(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  obtenerCurso(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/${id}`);
  }

  crearCurso(curso: any): Observable<any> {
    return this.http.post(this.apiUrl, curso);
  }

  actualizarCurso(id: number, curso: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, curso);
  }

  eliminarCurso(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}