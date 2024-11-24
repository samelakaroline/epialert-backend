# dashboards/service.py
import matplotlib.pyplot as plt
import io
from alerts.models import Alert
from django.utils.timezone import now, timedelta

def generate_weekly_alerts_chart():
    # Filtrar alertas da última semana
    last_week = now() - timedelta(days=7)
    alerts = Alert.objects.filter(created_at__gte=last_week)

    # Contar alertas por criticidade
    high = alerts.filter(severity__iexact='Alta').count()
    medium = alerts.filter(severity__iexact='Média').count()
    low = alerts.filter(severity__iexact='Baixa').count()

    # Configurar dados do gráfico
    labels = ['Alta', 'Média', 'Baixa']
    sizes = [high, medium, low]
    colors = ['#FF8042', '#FFBB28', '#0088FE']

    # Criar o gráfico
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Gráfico circular

    # Salvar o gráfico em memória
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return buffer
