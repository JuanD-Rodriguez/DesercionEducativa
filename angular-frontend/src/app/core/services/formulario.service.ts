// src/app/core/services/formulario.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FormularioService {
  private apiUrl = 'http://localhost:5000/formulario';

  constructor(private http: HttpClient) {}

  crearFormulario(formulario: any): Observable<any> {
    const token = localStorage.getItem('token');
    
    // Usar estructura_json directamente si ya viene del componente
    const payload = {
      titulo: formulario.titulo,
      descripcion: formulario.descripcion,
      estructura_json: formulario.estructura_json
    };

    console.log('Payload enviado al backend:', payload);

    return this.http.post(`${this.apiUrl}/crear`, payload, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
  }

  obtenerFormularios(): Observable<any[]> {
    const token = localStorage.getItem('token');
    return this.http.get<any[]>(`${this.apiUrl}/formularios`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  obtenerFormulario(id: number): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.get<any>(`${this.apiUrl}/formularios/${id}`, { headers });
  }

  getPreguntas(id_formulario: number): Observable<any[]> {
    const token = localStorage.getItem('token');
    return this.http.get<any[]>(`${this.apiUrl}/${id_formulario}/preguntas`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  enviarRespuestas(id_formulario: number, respuestas: any): Observable<any> {
    const token = localStorage.getItem('token');
    return this.http.post(`${this.apiUrl}/${id_formulario}/responder`, {
      respuestas_json: respuestas
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  eliminarFormulario(id: number): Observable<any> {
    const token = localStorage.getItem('token');
    return this.http.delete(`${this.apiUrl}/${id}/eliminar`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  cambiarEstado(id: number, nuevoEstado: string): Observable<any> {
    const token = localStorage.getItem('token');
    return this.http.put(`${this.apiUrl}/${id}/estado`, { estado: nuevoEstado }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  }
}