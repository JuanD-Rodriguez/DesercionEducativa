import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry, tap } from 'rxjs/operators';

export interface Usuario {
  id?: number;
  id_usuario?: number;
  id_estudiante?: number;
  nombre: string;
  apellido?: string;
  correo?: string;
  correo_electronico?: string;
  contrasena?: string;
  rol_id?: number;
  id_rol?: number;
  telefono?: string;
  id_ingenieria?: number;
  ingenieria?: string;
  promedio?: number;
  fecha_registro?: string;
}

@Injectable({
  providedIn: 'root'
})
export class UsuarioService {
  // Usamos la URL sin /api/ ya que así está configurado en tu backend
  private apiUrl = 'http://localhost:5000/usuarios';

  constructor(private http: HttpClient) {}

  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    })
  };

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Ocurrió un error desconocido';

    if (error.error instanceof ErrorEvent) {
      errorMessage = `Error: ${error.error.message}`;
    } else {
      errorMessage = `Código de estado: ${error.status}, Mensaje: ${error.message}`;
      if (error.error && typeof error.error === 'object' && error.error.mensaje) {
        errorMessage = error.error.mensaje;
      }
    }

    console.error('Error en la petición HTTP:', error);
    console.error('Mensaje de error:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }

  getUsuarios(): Observable<Usuario[]> {
    console.log('Obteniendo estudiantes de:', `${this.apiUrl}/estudiantes`);
    return this.http.get<Usuario[]>(`${this.apiUrl}/estudiantes`, this.httpOptions)
      .pipe(
        tap(data => console.log('Datos recibidos de estudiantes:', data)),
        retry(1),
        catchError(this.handleError)
      );
  }

  getUsuario(id: number): Observable<Usuario> {
    return this.http.get<Usuario>(`${this.apiUrl}/estudiante/${id}`, this.httpOptions)
      .pipe(
        retry(1),
        catchError(this.handleError)
      );
  }

  crearUsuario(usuario: any): Observable<any> {
    const datosParaBackend = {
      tipo: "estudiante",
      nombre: usuario.nombre,
      apellido: usuario.apellido || usuario.apellidos,
      correo_electronico: usuario.correo || usuario.correo_electronico,
      id_ingenieria: usuario.id_ingenieria || 1,
      telefono: usuario.telefono,
      promedio: usuario.promedio || 0
    };

    console.log('Datos enviados al servidor:', datosParaBackend);

    return this.http.post(`${this.apiUrl}/crear`, datosParaBackend, this.httpOptions)
      .pipe(
        tap(response => console.log('Respuesta de crear usuario:', response)),
        catchError(this.handleError)
      );
  }

  actualizarUsuario(id: number, usuario: any): Observable<any> {
    console.log(`Actualizando usuario con ID ${id}:`, usuario);

    if (!id) {
      console.error('ID de usuario no definido en actualizarUsuario');
      return throwError(() => new Error('ID de usuario no definido'));
    }

    return this.http.put(`${this.apiUrl}/actualizar/${id}`, usuario, {
      headers: this.httpOptions.headers
    }).pipe(
      catchError(this.handleError)
    );
  }

  eliminarUsuario(id: number): Observable<any> {
    console.log(`Eliminando usuario con ID ${id}`);

    if (!id) {
      console.error('ID de usuario no definido en eliminarUsuario');
      return throwError(() => new Error('ID de usuario no definido'));
    }

    return this.http.delete(`${this.apiUrl}/eliminar/${id}`, {
      headers: this.httpOptions.headers
    }).pipe(
      catchError(this.handleError)
    );
  }

  obtenerIngenierias(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/ingenierias`, this.httpOptions)
      .pipe(
        retry(1),
        catchError(this.handleError)
      );
  }

  // Método simplificado para crear un estudiante de prueba
  crearEstudiantePrueba(): Observable<any> {
    const estudiante = {
      tipo: "estudiante",
      nombre: "Estudiante",
      apellido: "Prueba",
      correo_electronico: `estudiante.prueba.${Math.floor(Math.random() * 1000)}@ejemplo.com`,
      id_ingenieria: 1,
      promedio: 3.5
    };

    return this.http.post(`${this.apiUrl}/crear`, estudiante, this.httpOptions)
      .pipe(
        tap(response => console.log('Estudiante de prueba creado:', response)),
        catchError(this.handleError)
      );
  }
}