import { Component, OnInit } from '@angular/core';
import { ReportesService } from 'src/app/core/services/reportes.service';
import { Chart, registerables } from 'chart.js';

// Registrar los componentes necesarios de Chart.js
Chart.register(...registerables);

@Component({
  selector: 'app-reportes',
  templateUrl: './reportes.component.html',
  styleUrls: ['./reportes.component.css']
})
export class ReportesComponent implements OnInit {
  // Variables para almacenar datos de reportes
  estadisticasGenerales: any = {};
  reportesPorIngenieria: any[] = [];
  factoresDesercion: any[] = [];
  estudiantesAltoRiesgo: any[] = [];

  // Variables para gráficos
  graficoPorIngenieria: any;
  graficoFactores: any;
  
  // Estados de carga
  cargandoEstadisticas: boolean = true;
  cargandoIngenieria: boolean = true;
  cargandoFactores: boolean = true;
  cargandoEstudiantes: boolean = true;

  constructor(private reportesService: ReportesService) { }

  ngOnInit(): void {
    this.cargarEstadisticasGenerales();
    this.cargarDesercionPorIngenieria();
    this.cargarFactoresDesercion();
    this.cargarEstudiantesAltoRiesgo();
  }

  cargarEstadisticasGenerales(): void {
    this.reportesService.obtenerEstadisticasGenerales().subscribe({
      next: (data) => {
        this.estadisticasGenerales = data;
        this.cargandoEstadisticas = false;
      },
      error: (error) => {
        console.error('Error al cargar estadísticas generales:', error);
        this.cargandoEstadisticas = false;
      }
    });
  }

  cargarDesercionPorIngenieria(): void {
    this.reportesService.obtenerDesercionPorIngenieria().subscribe({
      next: (data) => {
        this.reportesPorIngenieria = data;
        this.cargandoIngenieria = false;
        this.crearGraficoPorIngenieria();
      },
      error: (error) => {
        console.error('Error al cargar deserción por ingeniería:', error);
        this.cargandoIngenieria = false;
      }
    });
  }

  cargarFactoresDesercion(): void {
    this.reportesService.obtenerFactoresDesercion().subscribe({
      next: (data) => {
        this.factoresDesercion = data;
        this.cargandoFactores = false;
        this.crearGraficoFactores();
      },
      error: (error) => {
        console.error('Error al cargar factores de deserción:', error);
        this.cargandoFactores = false;
      }
    });
  }

  cargarEstudiantesAltoRiesgo(): void {
    this.reportesService.obtenerEstudiantesAltoRiesgo(0.7).subscribe({
      next: (data) => {
        this.estudiantesAltoRiesgo = data;
        this.cargandoEstudiantes = false;
      },
      error: (error) => {
        console.error('Error al cargar estudiantes en alto riesgo:', error);
        this.cargandoEstudiantes = false;
      }
    });
  }

  crearGraficoPorIngenieria(): void {
    if (!this.reportesPorIngenieria || this.reportesPorIngenieria.length === 0) return;

    // Preparar datos para el gráfico
    const labels = this.reportesPorIngenieria.map(item => item.nombre_ingenieria);
    const riesgoPromedio = this.reportesPorIngenieria.map(item => item.riesgo_promedio * 100);
    const porcentajeRiesgo = this.reportesPorIngenieria.map(item => item.porcentaje_alto_riesgo);

    // Crear el gráfico de barras
    const ctx = document.getElementById('graficoIngenieria') as HTMLCanvasElement;
    this.graficoPorIngenieria = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Riesgo Promedio (%)',
            data: riesgoPromedio,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          },
          {
            label: 'Estudiantes en Alto Riesgo (%)',
            data: porcentajeRiesgo,
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  }

  crearGraficoFactores(): void {
    if (!this.factoresDesercion || this.factoresDesercion.length === 0) return;

    // Preparar datos para el gráfico
    const labels = this.factoresDesercion.map(item => item.factor);
    const cantidades = this.factoresDesercion.map(item => item.cantidad);

    // Crear el gráfico de pastel
    const ctx = document.getElementById('graficoFactores') as HTMLCanvasElement;
    this.graficoFactores = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          data: cantidades,
          backgroundColor: [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true
      }
    });
  }

  exportarPDF(): void {
    // Aquí iría la lógica para exportar a PDF
    alert('Función de exportar a PDF no implementada aún');
  }

  exportarExcel(): void {
    // Aquí iría la lógica para exportar a Excel
    alert('Función de exportar a Excel no implementada aún');
  }
}