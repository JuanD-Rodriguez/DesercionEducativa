import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    // Obtener roles permitidos de los datos de la ruta
    const allowedRoles = route.data['roles'] as Array<number>;
    
    // Verificar si el usuario tiene uno de los roles permitidos
    const userRole = this.authService.getUserRole();
    
    if (userRole !== null && allowedRoles.includes(userRole)) {
      return true;
    }
    
    // Si el usuario está logueado pero no tiene el rol adecuado,
    // redirigir según su rol
    if (this.authService.isLoggedIn()) {
      this.authService.navigateByRole();
    } else {
      // Si no está logueado, redirigir al login
      this.router.navigate(['/login']);
    }
    
    return false;
  }
}