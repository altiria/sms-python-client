![](http://static.altiria.com/wp-content/themes/altiria/images/logo-altiria.png)


# Altiria, cliente SMS Python

 ![](https://img.shields.io/badge/version-0.9.0-blue.svg)

Altiria SMS Python es un cliente que simplifica al máximo la integración de nuestro API para Python. Por el momento, esta librería abarca las funciones más básicas:
- **Envíos de SMS individuales** con las siguientes características:
  - sencillos
  - concatenados
  - certificación de entrega con o sin identificador
  - certificado digital de entrega
  - uso de remitente
  - seleccionar codificación
- **Consultas de crédito**

## Requisitos

- python 2.7+, 3.+.

## Instalación

La forma recomendada de instalar el cliente Altiria para Python es a través de **pip** .

### Si tienes PIP instalado

<pre>
sudo pip install sms-php-client
</pre>

### Si no tienes PIP instalado

<pre>
git clone https://github.com/altiria/sms-python-client.git

cd sms-python-client

python setup.py install
</pre>

## Ejemplos de uso

### Envío de SMS

A continuación se describen cada una de las posibilidades de uso de la librería para realizar envíos de SMS.

#### Ejemplo básico

Se trata de la opción más sencilla para realizar un envío de SMS.

```python
from sms_api.altiria_client import *

try:
	client = AltiriaClient('miusuario@email.com', 'contraseña')
	textMessage = AltiriaModelTextMessage('346XXXXXXXX', 'Mensaje de prueba')
	jsonText = client.sendSms(textMessage)
	print('¡Mensaje enviado!')

except AltiriaGwException as ae:
	print('Mensaje no aceptado:'+ae.message)
	print('Código de error:'+ae.status)
except JsonException as je:
	print('Error en la petición:'+je.message)
except ConnectionException as ce:
	if "RESPONSE_TIMEOUT" in ce.message: 
		print('Tiempo de respuesta agotado:'+ce.message)
	else:
		print('Tiempo de conexión agotado:'+ce.message)
```

#### Ejemplo básico con timeout personalizado

Permite fijar el tiempo de respuesta en milisegundos. Si se supera se lanzará una **ConnectionException**.
Por defecto el tiempo de respuesta es de 10 segundos, pero puede ser ajustado entre 1 y 30 segundos.

```python
from sms_api.altiria_client import *

try:
	client = AltiriaClient('miusuario@email.com', 'contraseña', 5000)
	textMessage = AltiriaModelTextMessage('346XXXXXXXX', 'Mensaje de prueba')
	jsonText = client.sendSms(textMessage)
	print('¡Mensaje enviado!')

except AltiriaGwException as ae:
	print('Mensaje no aceptado:'+ae.message)
	print('Código de error:'+ae.status)
except JsonException as je:
	print('Error en la petición:'+je.message)
except ConnectionException as ce:
	if "RESPONSE_TIMEOUT" in ce.message: 
		print('Tiempo de respuesta agotado:'+ce.message)
	else:
		print('Tiempo de conexión agotado:'+ce.message)
```

#### Ejemplo básico con remitente

Se trata de la opción más sencilla para realizar un envío de SMS añadiendo remitente.

```python
from sms_api.altiria_client import *

try:
	client = AltiriaClient('miusuario@email.com', 'contraseña')
	textMessage = AltiriaModelTextMessage('346XXXXXXXX', 'Mensaje de prueba', 'miRemitente')
	jsonText = client.sendSms(textMessage)
	print('¡Mensaje enviado!')

except AltiriaGwException as ae:
	print('Mensaje no aceptado:'+ae.message)
	print('Código de error:'+ae.status)
except JsonException as je:
	print('Error en la petición:'+je.message)
except ConnectionException as ce:
	if "RESPONSE_TIMEOUT" in ce.message: 
		print('Tiempo de respuesta agotado:'+ce.message)
	else:
		print('Tiempo de conexión agotado:'+ce.message)
```
#### Ejemplo con todos los parámetros

Se muestra un ejemplo utilizando todo los parámetros e integrando el módulo de **logging**.
La implementación de este módulo permite depurar el log de la librería.

```python
from sms_api.altiria_client import *
import logging

logging.basicConfig(filename='app.log',
                            filemode='a',
                            format='%(asctime)s %(levelname)s %(module)s.%(funcName)s:%(lineno)d [%(thread)d, %(threadName)s] - %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S',
                            level=logging.DEBUG)

try:
    logging.debug('Enviando SMS...')

	client = AltiriaClient('miusuario@email.com', 'contraseña')
	client.setConnectionTimeout(1000)
	client.setTimeout(5000)
	textMessage = AltiriaModelTextMessage('346XXXXXXXX', 'Mensaje de prueba')
	textMessage.senderId='miRemitente'
	textMessage.ack=True
	textMessage.idAck='idAck'
	textMessage.concat=True
	textMessage.encoding='unicode'
	textMessage.certDelivery=True
	jsonText = client.sendSms(textMessage)
	print('¡Mensaje enviado!')

except AltiriaGwException as ae:
	print('Mensaje no aceptado:'+ae.message)
	print('Código de error:'+ae.status)
except JsonException as je:
	print('Error en la petición:'+je.message)
except ConnectionException as ce:
	if "RESPONSE_TIMEOUT" in ce.message: 
		print('Tiempo de respuesta agotado:'+ce.message)
	else:
		print('Tiempo de conexión agotado:'+ce.message)
```
### Consulta de crédito

A continuación se describen cada una de las posibilidades de uso de la librería para consultar el crédito.

#### Ejemplo básico

Este ejemplo no incluye los parámetros opcionales.

```python
from sms_api.altiria_client import *

try:
	client = AltiriaClient('miusuario@email.com', 'contraseña')
	credit = client.getCredit()
	print('Crédito disponible: '+credit)

except AltiriaGwException as ae:
	print('Solicitud no aceptada:'+ae.message)
	print('Código de error:'+ae.status)
except JsonException as je:
	print('Error en la petición:'+je.message)
except ConnectionException as ce:
	if "RESPONSE_TIMEOUT" in ce.message: 
		print('Tiempo de respuesta agotado:'+ce.message)
	else:
		print('Tiempo de conexión agotado:'+ce.message)
```

#### Ejemplo con todos los parámetros

Este ejemplo incluye los parámetros opcionales.

```python
from sms_api.altiria_client import *

try:
	client = AltiriaClient('miusuario@email.com', 'contraseña')
    client.setConnectionTimeout(1000)
	client.setTimeout(5000)
	credit = client.getCredit()
	print('Crédito disponible: '+credit)

except AltiriaGwException as ae:
	print('Solicitud no aceptada:'+ae.message)
	print('Código de error:'+ae.status)
except JsonException as je:
	print('Error en la petición:'+je.message)
except ConnectionException as ce:
	if "RESPONSE_TIMEOUT" in ce.message: 
		print('Tiempo de respuesta agotado:'+ce.message)
	else:
		print('Tiempo de conexión agotado:'+ce.message)
```

## Licencia

La licencia de esta librería es de tipo MIT. Para más información consultar el fichero de licencia.

## Ayuda

Utilizamos la sección de problemas de GitHub para tratar errores y valorar nuevas funciones.
Para cualquier problema durante la intergración contactar a través del email soporte@altiria.com.
