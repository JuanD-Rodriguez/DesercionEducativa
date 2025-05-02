// src/app/gestor/reportes/dashboard-reportes.component.ts
import { Component, OnInit } from '@angular/core';
import { ReportesService } from 'src/app/core/services/reportes.service';

@Component({
  selector: 'app-dashboard-reportes',
  templateUrl: './dashboard-reportes.component.html',
  styleUrls: ['./dashboard-reportes.component.css']
})
export class DashboardReportesComponent implements OnInit {
  estadisticasGenerales: any = {};
  factoresDesercion: any[] = [];
  desercionPorIngenieria: any[] = [];
  cargando = true;

  constructor(private reportesService: ReportesService) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos(): void {
    // Cargar estadísticas generales
    this.reportesService.obtenerEstadisticasGenerales().subscribe({
      next: (data) => {
        this.estadisticasGenerales = data;
        this.cargando = false;
      },
      error: (err) => {
        console.error('Error al cargar estadísticas generales:', err);
        this.cargando = false;
      }
    });

    // Cargar factores de deserción
    this.reportesService.obtenerFactoresDesercion().subscribe({
      next: (data) => {
        this.factoresDesercion = data;
      },
      error: (err) => {
        console.error('Error al cargar factores de deserción:', err);
      }
    });

    // Cargar deserción por ingeniería
    this.reportesService.obtenerDesercionPorIngenieria().subscribe({
      next: (data) => {
        this.desercionPorIngenieria = data;
      },
      error: (err) => {
        console.error('Error al cargar deserción por ingeniería:', err);
      }
    });
  }

  calcularPorcentaje(cantidad: number, total: number): string {
    if (total === 0) return '0%';
    return ((cantidad / total) * 100).toFixed(1) + '%';
  }
}