![](http://static.altiria.com/wp-content/themes/altiria/images/logo-altiria.png)


# Altiria, cliente SMS Python

Para poder utilizar nuestro servicio es necesario previamente crear una cuenta en Altiria. Es habitual crear una **cuenta de prueba** en la que cargamos una serie de créditos de manera gratuita para que puedas realizar pruebas durante la integración.

Cabe mencionar que este proyecto consta de una **sección de tests** que al ser lanzados pueden suponer un **consumo de créditos**. En concreto, son los test "TestSendSmsHttp.test_ok_mandatory_params" y "TestSendSmsHttp.test_ok_all_params" que al ser lanzados consumirán un mínimo de tres créditos. Este consumo puede verse incrementado si se habilita la características "certDelivery" comentada en el test "TestSendSmsHttp.test_ok_all_params", para certificar la entrega del SMS.

Antes de lanzar los tests es necesario **parametrizar cada suite** modificando las variables definidas en el archivo "__init_.py" bajo el comentario "configurable parameters".
Los parámetros a configurar son los siguientes:
- login: email de la cuenta.
- password: contraseña de la cuenta.
- destination: teléfono destino. Es importante agregar el prefijo internacional y no incluir ningún símbolo ni espacio. Ejemplo: '346XXXXXXXX'.
- sender: (opcional) remitente. Sólo se debe asignar un valor para el remitente si ha sido previamente autorizado por Altiria. En caso contrario asignar None como valor.
- debug: si se le asigna el valor true, se mostrará información adicional por consola que puede resultar interesante para depurar.

Finalmente, para correr todos los tests ejecutar el comando **make tests** desde el directorio raíz del proyecto.




