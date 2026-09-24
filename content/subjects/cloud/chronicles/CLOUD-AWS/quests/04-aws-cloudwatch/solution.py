import logging

# 1. Observabilidad: Inicializado globalmente para reúso de contenedores Lambda
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Recibe el evento, procesa las reglas de negocio y envía los logs 
    estructurados correspondientes hacia Amazon CloudWatch.
    """
    try:
        # Extraemos información de negocio
        dragon_id = event.get('dragon_id')
        inestabilidad = int(event.get('inestabilidad', 0))
        
        # Log normal hacia CloudWatch Log Stream
        logger.info(f"Procesando reporte del dragón ID: {dragon_id}")
        
        # Regla de Alarma
        if inestabilidad >= 90:
            # Este texto exacto activa el Metric Filter en AWS
            logger.error(f"¡PELIGRO CRÍTICO! Dragón {dragon_id} a punto de explotar. Nivel: {inestabilidad}")
            # Rompemos el flujo para que Lambda se marque como Fallida en las métricas de invocación
            raise Exception("Inestabilidad catastrófica")
            
        logger.info("Estado normal. Finalizando.")
        return {'statusCode': 200}
        
    except Exception as e:
        logger.error(f"Fallo en el pipeline: {str(e)}")
        return {'statusCode': 500}
