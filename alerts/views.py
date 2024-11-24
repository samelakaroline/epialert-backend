from datetime import timedelta
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from alerts.models import Alert
from .serializers import AlertSerializer

# URLs das APIs
MINISTRY_API_URL = "https://apidadosabertos.saude.gov.br/v1/"
DISEASE_SH_API_URL = "https://disease.sh/v3/covid-19/"

class LocalAlertsView(APIView):
    def get(self, request):
        try:
            # Buscar dados de arboviroses
            response = requests.get(f"{MINISTRY_API_URL}arboviroses/")
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException:
            return Response({"error": "Não foi possível obter os dados locais."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GlobalAlertsView(APIView):
    def get(self, request):
        try:
            # Buscar dados globais
            response = requests.get(f"{DISEASE_SH_API_URL}countries")
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException:
            return Response({"error": "Não foi possível obter os dados globais."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CombinedAlertsView(APIView):
    def get(self, request):
        try:
            # Buscar dados de ambas as APIs
            local_response = requests.get(f"{MINISTRY_API_URL}arboviroses/")
            global_response = requests.get(f"{DISEASE_SH_API_URL}countries")
            local_data = local_response.json() if local_response.ok else []
            global_data = global_response.json() if global_response.ok else []

            # Combinar os dados
            combined_data = {
                "local_alerts": local_data,
                "global_alerts": global_data,
            }
            return Response(combined_data, status=status.HTTP_200_OK)
        except requests.RequestException:
            return Response({"error": "Não foi possível obter os dados combinados."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AlertsMetricsView(APIView):
    def get(self, request):
        try:
            # Consultar alertas no banco de dados para os últimos 7 dias
            last_week = now() - timedelta(days=7)

            # Normalizar status e severidade
            status_to_filter_verified = ['verified', 'verificado']
            status_to_filter_not_verified = ['not_verified', 'não verificado', 'nao verificado']
            severity_high = ['Alta', 'alta']
            severity_medium = ['Média', 'média', 'Media', 'media']
            severity_low = ['Baixa', 'baixa']

            # Consultar alertas no banco de dados
            total_alerts = Alert.objects.count()
            verified_alerts = Alert.objects.filter(status__in=status_to_filter_verified).count()
            not_verified_alerts = Alert.objects.filter(status__in=status_to_filter_not_verified).count()
            recent_alerts = Alert.objects.filter(created_at__gte=last_week)

            # Contar alertas recentes por criticidade
            recent_high = recent_alerts.filter(severity__in=severity_high).count()
            recent_medium = recent_alerts.filter(severity__in=severity_medium).count()
            recent_low = recent_alerts.filter(severity__in=severity_low).count()

            # Consultar dados externos
            response = requests.get(f"{DISEASE_SH_API_URL}countries")
            if response.status_code == 200:
                data = response.json()

                total_cases = sum(item['cases'] for item in data)
                total_recovered = sum(item['recovered'] for item in data)

                # Taxa de resolução de casos
                resolved_rate = (total_recovered / total_cases) * 100 if total_cases > 0 else 0

                # Retornar métricas
                return Response({
                    "resolved_alerts_rate": round(resolved_rate, 2),
                    "recent_alerts_weekly": {
                        "high": recent_high,
                        "medium": recent_medium,
                        "low": recent_low,
                    },
                    "active_alerts": not_verified_alerts,
                    "verified_alerts": verified_alerts,
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Erro ao buscar dados da API externa"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AlertsListView(APIView):
    def get(self, request):
        try:
            # Normalizar valores de status e severidade
            status_to_filter = ['verified', 'verificado', 'not_verified', 'não verificado', 'nao verificado']
            severity_high = ['Alta', 'alta']
            severity_medium = ['Média', 'média', 'Media', 'media']
            severity_low = ['Baixa', 'baixa']

            # Filtrar alertas
            alerts = Alert.objects.filter(
                status__in=status_to_filter,
                severity__in=severity_high + severity_medium + severity_low
            )

            serializer = AlertSerializer(alerts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
