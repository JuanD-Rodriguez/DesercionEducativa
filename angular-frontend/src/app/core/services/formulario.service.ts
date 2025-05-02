import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FormularioService {
  private apiUrl = 'http://localhost:5000/formulario';

  constructor(private http: HttpClient) { }

  /**
   * Obtiene todos los formularios
   * @returns Observable con la lista de formularios
   */
  obtenerFormularios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/formularios`);
  }

  /**
   * Obtiene un formulario específico por su ID
   * @param id ID del formulario
   * @returns Observable con el detalle del formulario
   */
  obtenerFormulario(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/formularios/${id}`);
  }

  /**
   * Crea un nuevo formulario
   * @param formulario Datos del formulario a crear
   * @returns Observable con la respuesta del servidor
   */
  crearFormulario(formulario: any): Observable<any> {
    return new Observable(observer => {
      // Datos absolutamente mínimos
      const datos = {
        titulo: "Test",
        preguntas: [{
          texto: "Test",
          categoria: "academico"
        }]
      };
      
      // Usar Fetch API para evitar problemas con HttpClient
      const token = localStorage.getItem('token');
      
      fetch('http://localhost:5000/formulario/crear', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(datos)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`Error HTTP: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        observer.next(data);
        observer.complete();
      })
      .catch(error => {
        console.error('Error en fetch:', error);
        observer.error(error);
      });
    });
  }
  /**
   * Elimina un formulario
   * @param id ID del formulario a eliminar
   * @returns Observable con la respuesta del servidor
   */
  eliminarFormulario(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/formularios/${id}`);
  }

  /**
   * Activa o desactiva un formulario
   * @param id ID del formulario
   * @param estado Nuevo estado (true = activo, false = inactivo)
   * @returns Observable con la respuesta del servidor
   */
  cambiarEstado(id: number, estado: boolean): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/formularios/${id}/estado`, { activo: estado });
  }

  /**
   * Obtiene las preguntas de un formulario
   * @param idFormulario ID del formulario (opcional)
   * @returns Observable con las preguntas
   */
  getPreguntas(idFormulario?: number): Observable<any[]> {
    let url = `${this.apiUrl}/preguntas`;
    if (idFormulario) {
      url += `?id_formulario=${idFormulario}`;
    }
    return this.http.get<any[]>(url);
  }

  /**
   * Envía las respuestas de un estudiante a un formulario
   * @param respuestas Respuestas del estudiante
   * @returns Observable con la respuesta del servidor
   */
  enviarRespuestas(respuestas: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/respuestas`, { respuestas });
  }
  
  /**
   * Obtiene las respuestas de un formulario
   * @param id ID del formulario
   * @returns Observable con las respuestas del formulario
   */
  obtenerRespuestas(id: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/respuestas/formulario/${id}`);
  }
}