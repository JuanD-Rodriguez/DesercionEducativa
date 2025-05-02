import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthService {
  // URL base para las peticiones de autenticación
  private apiUrl = 'http://localhost:5000/auth';

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

  login(usuario: string, contrasena: string): Observable<any> {
    return this.http.post<{ access_token: string }>(`${this.apiUrl}/login`, {
      nombre_usuario: usuario,
      contrasena: contrasena
    }).pipe(
      tap(res => localStorage.setItem('token', res.access_token))
    );
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }

  isLoggedIn(): boolean {
    const token = localStorage.getItem('token');
    return !!token; // Simplificado por ahora
  }

  // Método para decodificar el token y obtener el rol del usuario
  getUserRole(): number | null {
    const token = localStorage.getItem('token');
    if (!token) return null;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      
      // Buscar el rol en el objeto sub (según el formato del token)
      if (payload.sub && typeof payload.sub === 'object' && payload.sub.rol !== undefined) {
        return payload.sub.rol;
      }
      
      // Si no está en sub, buscar directamente en el payload
      if (payload.rol !== undefined) {
        return payload.rol;
      }
      
      return null;
    } catch (error) {
      console.error('Error al decodificar el token', error);
      return null;
    }
  }

  // Método para redirigir según el rol del usuario
  navigateByRole(): void {
    const role = this.getUserRole();
    
    if (role === 1) {
      // Redirigir a admin usando navegación absoluta
      window.location.href = '/admin';
    } else if (role === 2) {
      // Redirigir a gestor usando navegación absoluta
      window.location.href = '/gestor';
    } else if (role === 3) {
      // Redirigir a estudiante usando navegación absoluta
      window.location.href = '/formulario-desercion';
    } else {
      // Si no se puede determinar el rol
      this.router.navigate(['/login']);
    }
  }

  enviarCodigo(correo: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/recuperar`, { correo });
  }
  
  verificarCodigo(correo: string, codigo: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/verificar-codigo`, { correo, codigo });
  }
  
  restablecerContrasena(correo: string, nueva_contrasena: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/restablecer-contrasena`, { correo, nueva_contrasena });
  }
}