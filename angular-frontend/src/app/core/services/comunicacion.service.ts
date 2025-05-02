import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ComunicacionService {
  private apiUrl = 'http://localhost:5000/api/comunicacion';

  constructor(private http: HttpClient) {}

  enviarMensaje(destinatario: number, asunto: string, contenido: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/enviar`, {
      id_destinatario: destinatario,
      asunto,
      contenido
    });
  }

  obtenerMensajesRecibidos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/recibidos`);
  }

  obtenerMensajesEnviados(): Observable<any> {
    return this.http.get(`${this.apiUrl}/enviados`);
  }

  marcarComoLeido(idMensaje: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/marcar_leido/${idMensaje}`, {});
  }

  obtenerMensaje(idMensaje: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/mensaje/${idMensaje}`);
  }
  
  // Añade este método para resolver el error
  obtenerMensajesEstudiante(): Observable<any[]> {
    // Por ahora devolvemos un array vacío simulado
    // Más adelante puedes implementar la llamada real a la API
    return of([]);
    
    // Cuando implementes el endpoint en el backend, puedes usar:
    // return this.http.get<any[]>(`${this.apiUrl}/estudiante/mensajes`);
  }
}