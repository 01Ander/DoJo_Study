def lambda_handler(event, context):
    """
    Función de entrada para AWS Lambda. Reacciona a un Trigger de S3,
    extrae el bucket y la llave, y retorna una respuesta de éxito 200.
    Si el payload es inválido, retorna 500.
    """
    try:
        # Extraemos quirúrgicamente del payload estándar de S3
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Lambda exige una estructura simulando una respuesta HTTP
        return {
            'statusCode': 200,
            'body': f'Archivo {key} subido a {bucket}'
        }
    except Exception:
        # Si el evento no tiene el formato esperado, evitamos que Lambda explote ruidosamente
        # y devolvemos un 500 ordenado.
        return {
            'statusCode': 500,
            'body': 'Error'
        }
