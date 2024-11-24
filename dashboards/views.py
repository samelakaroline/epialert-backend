from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from alerts.models import Alert
from django.utils.timezone import now, timedelta
import logging
from .service import generate_weekly_alerts_chart
from django.http import HttpResponse


# Configuração de log para depuração
logger = logging.getLogger(__name__)

class WeeklyAlertsPieChartView(APIView):
    def get(self, request):
        try:
            # Filtrar alertas da última semana (últimos 7 dias)
            last_week = now() - timedelta(days=7)

            # Normalizar os valores de status e severidade
            status_to_filter = ['not_verified', 'não verificado', 'nao verificado']
            severity_high = ['Alta', 'alta']
            severity_medium = ['Média', 'média', 'Media', 'media']
            severity_low = ['Baixa', 'baixa']

            # Buscar alertas não resolvidos com status normalizado
            unresolved_alerts = Alert.objects.filter(
                created_at__gte=last_week,
                status__in=status_to_filter
            )

            # Contar por criticidade com severidade normalizada
            high_criticality = unresolved_alerts.filter(
                severity__in=severity_high
            ).count()
            medium_criticality = unresolved_alerts.filter(
                severity__in=severity_medium
            ).count()
            low_criticality = unresolved_alerts.filter(
                severity__in=severity_low
            ).count()

            # Dados para o gráfico
            data = {
                "high": high_criticality,
                "medium": medium_criticality,
                "low": low_criticality,
            }

            # Log de depuração
            logger.debug(f"Dados do gráfico semanal: {data}")
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            # Log do erro
            logger.error(f"Erro ao processar os alertas semanais: {e}", exc_info=True)
            return Response({"error": f"Ocorreu um erro: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WeeklyAlertsChartView(APIView):
    def get(self, request):
        try:
            # Gera o gráfico utilizando o serviço criado
            chart_buffer = generate_weekly_alerts_chart()

            # Retornar o gráfico como resposta HTTP
            return HttpResponse(chart_buffer, content_type='image/png')
        except Exception as e:
            return HttpResponse(f"Erro ao gerar o gráfico: {e}", status=500)