Crear base de datos.
credenciales: 'practicante', '123'

Configurar opciones de base de datos.
Instalar oracle-instant-client.
Actualizar variables de entorno.
Modificar archivo sqlnet.ora en oracle/network/admin:
	Original Entry - SQLNET.AUTHENTICATION_SERVICES= (NTS)
	Modified Entry - SQLNET.AUTHENTICATION_SERVICES= (NONE)
Probar conexión y migrar al modelo:
python manage.py inspectdb > models.py
