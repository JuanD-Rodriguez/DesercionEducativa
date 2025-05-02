import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReportesService {
  private apiUrl = 'http://localhost:5000/api/reportes';

  constructor(private http: HttpClient) {}

  obtenerReportesDesercion(): Observable<any> {
    return this.http.get(`${this.apiUrl}/desercion`);
  }

  obtenerEstudiantesAltoRiesgo(umbral: number = 0.7): Observable<any> {
    return this.http.get(`${this.apiUrl}/desercion/alto_riesgo?umbral=${umbral}`);
  }

  obtenerDesercionPorIngenieria(): Observable<any> {
    return this.http.get(`${this.apiUrl}/desercion/por_ingenieria`);
  }

  obtenerFactoresDesercion(): Observable<any> {
    return this.http.get(`${this.apiUrl}/factores_desercion`);
  }

  obtenerAnalisisRespuestas(): Observable<any> {
    return this.http.get(`${this.apiUrl}/respuestas_analisis`);
  }

  obtenerEstadisticasGenerales(): Observable<any> {
    return this.http.get(`${this.apiUrl}/estadisticas_generales`);
  }
}