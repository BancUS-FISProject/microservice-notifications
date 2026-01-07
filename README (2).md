# Documentacion 

| **Autores**              | **Microservicios Implementados**                                              |
|:-------------------------|:------------------------------------------------------------------------------|
| **Pablo Medinilla Mejías** | Microservicio cards, Frontend común completo |

---

Descripción concreta de lo que ha hecho cada uno.

## 1. Nivel de Acabado

La entrega se plantea con el microservicio Cards completamente funcional y con integración en la arquitectura global (API Gateway + resto de microservicios), además del frontend común con rutas, navegación y pantallas que permiten ejecutar todas las operaciones relevantes del API de Cards.

**Acabado:** **10**, se incluyen  6 características del microservicio avanzado implementados y 4 características de la aplicación basada en microservicios avanzada implementados. 

El proyecto se presenta con la arquitectura base y los microservicios totalmente operativos:

* **API Gateway:** Implementado y funcional. Incluye lógica de *throttling* (limitación de peticiones por subscripcion), autenticación centralizada y enrutamiento al resto de microservicios.
* **Microservicio Accounts:** Funcionalidad completa CRUD, gestión de estados (bloqueo/desbloqueo) y endpoints dependientes de otros microservicios (Cards/Currencies).
* **Microservicio Currencies:** Actúa como adaptador/wrapper consumiendo la API externa para realizar conversiones reales, además de controlar el consumo de la API externa.
* **Mircroservcio Cards:** Funcionalidad completa CRUD, gestión de estados (active/frozen)

### Características implementadas

* **MICROSERVICIO BÁSICO QUE GESTIONE UN RECURSO** completo: La entrega incluye el microservicio Cards operativo en la arquitectura de microservicios, integrado con el API Gateway, persistencia NoSQL, autenticación centralizada, documentación de API, dockerización, y un frontend común con rutas y navegación para operar el recurso tarjeta desde la interfaz.
  
  * **El backend debe ser una API REST tal como se ha visto en clase implementando al menos los métodos GET, POST, PUT y DELETE y devolviendo un conjunto de códigos de estado adecuado.** --> [microservice cards/routes/cards.js](https://github.com/BancUS-FISProject/microservice-cards/blob/master/routes/cards.js) (incluye swagger también)
  * **La API debe tener un mecanismo de autenticación.** --> se realiza en la API GATEWAY
  * **Debe tener un frontend que permita hacer todas las operaciones de la API.** --> Frontend común ([BancUS-frontend/src/components/OverviewPage.jsx](https://github.com/BancUS-FISProject/BancUS-frontend/blob/master/src/components/OverviewPage.jsx)), Frontend individual cards ([BancUS-frontend/src/components/CardsPage.jsx](https://github.com/BancUS-FISProject/BancUS-frontend/blob/master/src/components/CardsPage.jsx))
  * **Debe estar desplegado y ser accesible desde la nube (ya sea de forma individual o como parte de la aplicación).** --> **AÑADIR ENLACE**
  * **La API que gestione el recurso también debe ser accesible en una dirección bien versionada.** --> http://localhost:3000/v1/cards/...
  * **Se debe tener una documentación de todas las operaciones de la API incluyendo las posibles peticiones y las respuestas recibidas** --> OpenApi Specification con Swagger ([microservice cards/routes/cards.js](https://github.com/BancUS-FISProject/microservice-cards/blob/master/routes/cards.js)) (**AÑADIR ENLACE AL SWAGGER DE CARDS**)
  * **Debe tener persistencia utilizando MongoDB u otra base de datos no SQL.** --> Uso de MongoDB con Atlas
  * **Deben validarse los datos antes de almacenarlos en la base de datos (por ejemplo, haciendo uso  de mongoose).**  --> [microservice cards/models/Card.js](https://github.com/BancUS-FISProject/microservice-cards/blob/master/models/Card.js)
  * **Debe haber definida una imagen Docker del proyecto**  --> Proyecto (**AÑADIR ENLACE A IMAGEN DOCKER PROYECTO**), Microservicio cards (pabmedmej/microservice-cards:latest)
  * **Gestión del código fuente: El código debe estar subido a un repositorio de Github siguiendo Github Flow** --> Proyecto (https://github.com/BancUS-FISProject), Cards (https://github.com/BancUS-FISProject/microservice-cards)
  * **Integración continua: El código debe compilarse, probarse y generar la imagen de Docker automáticamente usando GitHub Actions u otro sistema de integración continua en cada commit** --> Uso de Actions ([microservice cards/.github/workflows/ci-cards.yml](https://github.com/BancUS-FISProject/microservice-cards/blob/master/.github/workflows/ci-cards.yml))
  * **Debe haber pruebas de componente implementadas en Javascript para el código del backend utilizando Jest o similar. Como norma general debe haber tests para todas las funciones del API no triviales de la  aplicación. Probando tanto escenarios positivos como negativos. Las pruebas deben ser tanto in-process como out-of-process**. --> Uso de Jest. Tests internos ([microservice cards/tests/cards.api.test.js](https://github.com/BancUS-FISProject/microservice-cards/blob/master/tests/cards.api.test.js)), Tests externos ([microservice cards/tests/cards.api.test.js](https://github.com/BancUS-FISProject/microservice-cards/blob/master/tests/cards.external.test.js))

* **MICROSERVICIO AVANZADO QUE GESTIONE UN RECURSO (6):**
  * **Implementar un frontend con rutas y navegación.** --> Frontend común ([BancUS-frontend/src/components/OverviewPage.jsx](https://github.com/BancUS-FISProject/BancUS-frontend/blob/master/src/components/OverviewPage.jsx)), Frontend individual ([BancUS-frontend/src/components/CardsPage.jsx](https://github.com/BancUS-FISProject/BancUS-frontend/blob/master/src/components/CardsPage.jsx))
  * **Implementar cachés o algún mecanismo para optimizar el acceso a datos de otros recursos.** --> Uso de redis para todos los microservicios. Redis cards ([microservice cards/redisClient.js](https://github.com/BancUS-FISProject/microservice-cards/blob/master/redisClient.js))
  * **Consumir alguna API externa (distinta de las de los grupos de práctica) a través del backend o algún otro tipo de almacenamiento de datos en cloud como Amazon S3** --> Microservice-currencies
  * Implementar el patrón “rate limit” al hacer uso de servicios externos --> **ÁLVARO PON RUTA AL ARCHIVO Y LÍNEA DÓNDE EMPIEZA**
  * **Implementar el patrón “circuit breaker” en las comunicaciones con otros servicios.** --> **ÁLVARO PON RUTA AL ARCHIVO Y LÍNEA DÓNDE EMPIEZA**
  * Implementar mecanismos de gestión de la capacidad como throttling o feature toggles para rendimiento. --> **ÁLVARO PON RUTA AL ARCHIVO Y LÍNEA DÓNDE EMPIEZA**

* **APLICACIÓN BASADA EN MICROSERVICIOS BÁSICA:** Completo
  * **Interacción completa entre todos los microservicios de la aplicación integrando información. La integración debe realizarse a través del backend.** --> Realizado
  * **Tener un frontend común que integre los frontends de cada uno de los microservicios. Cada pareja debe ocuparse, al menos, de la parte específica de su microservicio en el frontend común.** --> Realizado.
  * **Permitir la suscripción del usuario a un plan de precios y adaptar automáticamente la funcionalidad de la aplicación según el plan de precios seleccionado.** --> Puede realizarse en la página principal (si no se ha realizado la autenticación - [BancUS-frontend/src/components/OverviewPage.jsx](https://github.com/BancUS-FISProject/BancUS-frontend/blob/master/src/components/OverviewPage.jsx)) y en la página de pricing ([BancUS-frontend/src/pages/PricingPage.jsx](https://github.com/BancUS-FISProject/BancUS-frontend/blob/master/src/pages/PricingPage.jsx))
* **APLICACIÓN BASADA EN MICROSERVICIOS AVANZADA (6):**
  * **Implementar un mecanismo de autenticación basado en JWT o equivalente.** --> Como se acordó en el último seguimiento, al ser realizado por todas las parejas, esta característica se considera de APLICACIÓN BASADA EN MICROSERVICIOS AVANZADA. **ALVARO PON ENLACE AL JWT AQUÍ**
  * **Incluir en el plan de precios límites de uso y aplicarlos automáticamente según la suscripción del usuario.** --> **ALVARO PON ENLACE A LINEAS DONDE SE LIMITA EL NÚMERO DE TARJETAS**
  * **Hacer uso de un API Gateway con funcionalidad avanzada como un mecanismo de throttling o de autenticación.** --> **ALVARO PON Nº DE LÍNEA EN CONCRETO** [api-gateway/nginx.conf](https://github.com/BancUS-FISProject/api-gateway/blob/main/nginx.conf) **Nº LÍNEA**
  * **Cualquier otra extensión a la aplicación basada en microservicios básica acordada previamente con el profesor** --> Sistema de logs comunes con Grafana (ver en contenedor de Grafana) **HAY OTRA FORMA DE VERLO ÁLVARO??** 

### Análisis justificativo de la suscripción óptima de las APIs del proyecto (Cards)

La suscripción óptima se define como la de menor coste que mantiene un margen de seguridad suficiente para la carga prevista en la demostración y para un escenario realista de crecimiento, evitando sobredimensionar gasto.

En el caso del microservicio **Cards**, las necesidades de APIs externas se concentran en dos frentes: la **mensajería de notificaciones** asociada a eventos de tarjeta (alta, congelación, reactivación, alertas antifraude) y, cuando existen operaciones en moneda distinta a la base, la **conversión de importes en divisa** (consumida a través del microservicio de divisas). 

#### Notificaciones por email: Twilio SendGrid Email API

Para notificaciones, la opción de referencia es **Twilio SendGrid Email API**, que ofrece un **Free Trial de 60 días** con un límite de **100 correos/día**; tras el periodo de prueba, se requiere migración a un plan de pago para continuidad. 

En el caso de uso de Cards, la carga típica en un entorno de evaluación académica es reducida. Aun asumiendo un flujo conservador de eventos operativos y de seguridad, el límite diario del trial cubre holgadamente la ejecución de la demo, pruebas funcionales y escenarios de validación durante el periodo de evaluación. Por ello, para la entrega del proyecto, la suscripción óptima es el **Free Trial**.

Si se continúa con un uso sostenido (más allá del periodo de 60 días) o un incremento notable de usuarios/eventos, la suscripción óptima pasa a ser **Essentials**, plan de entrada de pago comercializado desde **19,95 €/mes**.  La justificación se basa en que Cards genera notificaciones por eventos concretos y no por flujos continuos. Por tanto, el salto de plan se reserva para continuidad operativa y crecimiento.

#### Microservice Currencies - Conversión de divisas: RapidAPI (Currency Converter Pro1)

Para conversiones, una alternativa típica vía RapidAPI es **Currency Converter Pro1**, cuyo plan **Basic** ofrece **3.000 solicitudes/mes** (además de límites adicionales indicados por el proveedor).  En Transfers, la conversión suele ser un soporte auxiliar (por ejemplo, mostrar importes equivalentes o validar operaciones en otra divisa). Para justificar la suscripción óptima, el criterio técnico recomendado es **reducir llamadas externas** mediante cacheo de tipos de cambio (en redis), dado que el tipo de cambio no requiere refresco por operación individual en contextos no bursátiles. Con esta estrategia, el plan **Basic** suele ser suficiente en evaluación.

El salto a un plan superior (por ejemplo, **Pro** con **20.000 solicitudes/mes**) solo se justifica si el consumo mensual esperado, **ya descontado el efecto del cacheo**, supera el umbral de seguridad del plan Basic. Aun así, no será necesario.

#### Regla de decisión (estimación simple de consumo)

Para sostener el análisis con un criterio cuantitativo sencillo:

- Si `E` es el número de eventos que disparan correo al día y `D` los días de actividad del mes, el consumo mensual aproximado es:

  `Emails/mes ≈ E · D`

  El trial queda justificado mientras `E ≤ 100` y el horizonte temporal sea el del periodo de prueba. 

- Si `T` es el número de actualizaciones efectivas de tipo de cambio (tras cacheo) por día y `D` los días del mes:

  `Requests/mes ≈ T · D`

  Esto permite argumentar de forma transparente cuándo se mantiene **Basic** y cuándo procede pasar a **Pro**. 

Gracias al cacheo, no será necesario adquirir ningún plan que suponga un coste adicional.

#### Conclusión (suscripción óptima)

En consecuencia, para el flujo de Cards en una entrega académica, la suscripción óptima queda justificada como:

- **SendGrid Free Trial** para notificaciones (coste cero y volumen suficiente durante 60 días).   
- **Currency Converter Pro1 Basic** para divisas (3.000/mes), apoyado en cacheo para minimizar llamadas.   

En un escenario de explotación continuada o crecimiento, la migración natural es:

- **SendGrid Essentials** para continuidad del envío de correo.   
- **Currency Converter Pro1 Pro** si el consumo efectivo supera el umbral del plan Basic. 


## 2. Descripción de la Aplicación
El sistema consiste en una arquitectura de microservicios para una entidad bancaria (**BancUS**). Permite la gestión integral de cuentas bancarias, incluyendo la creación de usuarios, consultas de saldo, creación de tajetas, transacciones, transacciones con tarjetas, actualizaciones de estado, operaciones monetarias multidivisa y, en función del plan elegido, notificaciones, pagos programados y servicio antifraude.

El diseño separa la lógica de negocio principal (cuentas y operaciones) de servicios auxiliares (como la conversión de divisas) y del punto único de entrada (API Gateway). Esta descomposición facilita escalado independiente, tolerancia a fallos y evolución modular por equipos.


## 3. Descomposición y Arquitectura
El sistema se compone de los siguientes elementos. Se marcan en **negrita** los desarrollados por esta parte del equipo:

1.  **API Gateway:** Punto único de entrada. Protege la red interna y distribuye las peticiones.
2.  **Microservicio Accounts (Python/Quart):**
    * Encargado de la persistencia y lógica de las cuentas.
    * Maneja la validación estricta de datos (Pydantic).
    * Orquesta llamadas a *Cards* y *Currencies*.
3.  **Microservicio Currencies (Java/Spring Boot):**
    * Provee servicios de conversión de moneda.
    * Integra proveedores externos (RapidAPI).
4.  **Microservicio Cards (Node.js/Express)** 
    * gestión del recurso tarjeta (CRUD), estados (active/frozen) y operaciones asociadas a tarjetas.
    * Recibe peticiones de *Accounts*, *Transfers* y *anti-fraud*
5.  **Frontend común (React/Vite):** interfaz unificada con rutas y navegación. Incluye páginas específicas para cada microservicio


![Diagrama de Arquitectura de Cards](https://mermaid.live/edit#pako:eNp9k91u2jAUx1_F8hVINLRAwsfFJgio60QqVFgrLfTCTQ7gNdiZ7XRlVZ-qj9AX27FDu5RutRTFPv75fP3tB5rIFOiArhXLN2QxXgqCQxc3pWFJw4yDMLCk5Y4dwzyPh3nGE5bw5ydBouenO56RJrmCm-sSA5EuxTtfEU-U1KDueMIlSYEsmPoBhmlSC5lKdb0aZTqKp5KlZMQyJhJQ6P9MrBVofV1JZXYW40dOmYFfbIfM5D63jE2yyhVmE0c8TTPEFJCvVwtnqyBTueZJHEphlMxYKlU1wQp3CiLGD9QLMxueN8PL8MPKZ6A01wZEwlm1yAtIuY5r7kdClmygXgkVSbGWcc39xiMyU3zL1K7-YaQx5LjhAmlshgElmH6jXpLIQhgdzeNoTsIC1X1T37k0fFVuuqmTWQrQ78Nij8nREfmyWMzmzYvJfIH1_CxAG7R-QgFLajpyS5Rpfwr1cgbs_96CM-toIW9BkEuW8fRz6cJqsvdipxY68Ui4geS2bJfDXPtKrOykTYobUhszw-qHnl6RiGvtNl2DD8K0PARZ2rxS3MAh5aaWsgH-m2nbI9_yFG_mv1N95ToeuQTFV7sXbcr2vOp0gPsemWyxuskdSkdqQ70TSVnkXrqloA180DylA6MKaNAtqC2zS_pgfS2p2cAWn_QApymsWJEZe0Me8VjOxHcpty8nlSzWGzpYsUzjqnDVjDnDy_YXsddNhTZXOjjp-s4HHTzQe1z2-l4n6HbaQasXBH4raDfojg76Xr_d7fhBz_ePT1qdoPPYoL9d1GOv1_WPcbT6QasV-J3u4x-SfGaw)

## 4 Consumo

### 4.1. Customer Agreement (SLA e Interfaz)

**Formato de respuestas**
* Respuestas exitosas y de error en JSON.
* Errores consistentes y trazables (código, mensaje y, cuando proceda, detalle).

**Semántica HTTP**
* `200` para lecturas y actualizaciones con contenido.
* `201` para creación.
* `204` para operaciones sin contenido (por ejemplo, `freeze/unfreeze` si se decide sin body).
* `400` para validación y datos mal formados.
* `401` para no autenticado.
* `403` para autenticado sin permisos o por restricción de plan.
* `404` para recurso inexistente.
* `409` para conflictos de estado (por ejemplo, congelar una tarjeta ya congelada).
* `503` para dependencia no disponible cuando una operación requiere un servicio aguas abajo.

**Disponibilidad y degradación**
* Ante caída de dependencias, se devuelve error controlado con `503` y no se bloquea el servicio.
* Se recomiendan timeouts y reintentos limitados para evitar fallo en cascada.

### 4.2. Planes de precios 

Los planes definen límites y activación de capacidades. El backend se considera fuente de verdad, y el frontend refleja restricciones para mejorar la experiencia de uso.

| Plan | Precio | Límites y características funcionales | Extrafuncionales / capacidad |
|:--|:--:|:--|:--|
| **Básico** | 0 EUR/mes | 1 tarjeta virtual y hasta 5 operaciones/mes. Sin pagos programados, notificaciones y servicio antifraude | Límite de uso conservador y protección por plan |
| **Estudiante** | 4,99 EUR/mes | Hasta 5 tarjetas, hasta 20 operaciones/mes, notificaciones en tiempo real, servicio antifraude | Mayor capacidad y prioridad estándar |
| **Profesional** | 9,99 EUR/mes | Tarjetas ilimitadas, operaciones ilimitadas, pagos programados, antifraude ampliado, notificaciones avanzadas | Capacidad alta, sin límites y mejor experiencia |

**Aplicación automática de límites**
- Las políticas de plan se aplican en backend (y, si se decide, en el Gateway).
- El frontend deshabilita acciones no permitidas e informa del motivo (límite alcanzado, funcionalidad no incluida, etc.)

> **Acuerdo de Nivel de Servicio (SLA):**
> * **Disponibilidad:** El sistema está diseñado para responder con códigos 503 si un servicio dependiente cae, sin bloquear el hilo principal.
> * **Formato:** Todas las respuestas exitosas y de error siguen el estándar JSON.
> * **Errores:** Se implementan respuestas HTTP semánticas (400 Bad Request para validación, 404 Not Found para recursos inexistentes).

**Políticas de Consumo:**
* Se requiere autenticación previa en el Gateway.
* Las operaciones monetarias validan saldo antes de llamar al servicio de divisas.
* Validación estricta de tipos de datos en entrada (Strong Typing).

## 5 Frontend común (React + Vite)

El frontend común proporciona una interfaz unificada para operar los recursos expuestos por el sistema a través del **API Gateway**. La comunicación se realiza exclusivamente con endpoints versionados bajo `/v1`, evitando acceso directo a microservicios internos.

### 5.1 Finalidad y alcance
El frontend de **BancUS** implementa la interfaz web de la demo de microservicios. Su función es centralizar la interacción del usuario con los casos de uso de autenticación, perfil, cuentas, antifraude, notificaciones, pagos programados, tarjetas y transferencias, delegando la lógica de negocio en los microservicios correspondientes. 

### 5.2 Alcance funcional
El frontend cubre los flujos de autenticación (login y registro), perfil, cuentas, tarjetas, notificaciones, pagos programados, servicio antifraude, historial y transferencias, con envío de credenciales mediante token y persistencia de sesión en almacenamiento local del navegador. 

### Tecnologías

- React
- Vite
- JavaScript
- Cliente HTTP `fetch` 
- Docker 

### 5.3 Integración con el API Gateway (Nginx)

- Toda comunicación se realiza contra el Gateway con endpoints versionados `/v1/...`.
- Autenticación mediante token en cabecera `Authorization` (JWT).
- Gestión de errores coherente con el SLA (mensajes de validación, no autorizado, no encontrado, conflicto).


La integración de los microservicios con el **API Gateway** se realiza mediante *reverse proxy* en Nginx, de modo que el frontend y cualquier cliente consumen siempre el gateway como punto único de entrada. El objetivo es exponer el microservicio Cards bajo el prefijo versionado `/v1/microservicio`.

#### 1 Requisito de red (Docker)
Para que Nginx pueda resolver el host de cada microservicio, el contenedor del gateway y el contenedor del microservicio deben estar en **la misma red Docker**.

Ejemplo:
- `api-gateway` en la red `bankus-net`
- `microservice-cards` en la red `bankus-net`
- el servicio Cards expone internamente el puerto `3000`

### Gestión de sesión y credenciales
La sesión se gestiona mediante un token JWT que se persiste y reutiliza desde `localStorage`. Cuando existe, se adjunta en cabecera `Authorization: Bearer`. Asimismo, se persiste el perfil en `localStorage` (incluyendo IBAN), con utilidades de limpieza consistentes en eliminar `authToken` y `authUser`. 

### 5.4 Páginas principales y comportamiento
A efectos de documentación funcional, las pantallas principales pueden describirse por su propósito y las acciones que habilitan. En entornos sin sesión iniciada, la experiencia se restringe a navegación informativa y a los flujos de acceso.

| Página | Estado de acceso | Qué se muestra y para qué sirve | Acciones principales | Servicios/API implicados |
| :-- | :-- | :-- | :-- | :-- |
| Inicio (sin login) | Público | Vista de entrada con acceso limitado, orientada a explicar el propósito de la demo y conducir al inicio de sesión o al registro. Se evita exponer datos bancarios sin autenticación. | Ir a Login, ir a Registro | `user-auth` vía gateway  |
| Login | Público | Formulario de autenticación. Tras credenciales válidas, se almacena token y usuario para habilitar el resto de la navegación. | Iniciar sesión, validación de campos, gestión de error de credenciales | `/user-auth/auth/login` vía gateway  |
| Registro | Público | Alta de usuario. Tras creación, se habilita el paso a login o autenticación directa según el flujo implementado. | Crear usuario, validación de campos, mensajes de error | `/user-auth/users` vía gateway  |
| Panel principal (post-login) | Privado | Vista de aterrizaje tras autenticación con accesos a módulos: cuentas, perfil, tarjetas y transferencias. | Navegación entre módulos, cierre de sesión | Gateway y servicios externos según módulo  |
| Perfil | Privado | Consulta y edición de datos del usuario identificado, con operaciones sobre el identificador (IBAN) del perfil. | Ver perfil, editar perfil, persistir cambios | Lectura y `PATCH` a `user-auth` (por IBAN/identificador)  |
| Cuentas | Privado | Gestión de cuentas bancarias del usuario: listado y detalle. | Listar, consultar detalle, operaciones de cuenta según backend | `/accounts` vía gateway  |
| Transferencias | Privado | Gestión de transferencias y consulta de transacciones, desacoplada del gateway en el escenario descrito. | Crear transferencia, listar transacciones, manejar errores de disponibilidad | `VITE_TRANSFERS_API_BASE_URL` (servicio externo)  |
| Tarjetas | Privado | Módulo de tarjetas consumiendo el servicio de cards. En el escenario base, no se enruta por el gateway, por lo que depende del despliegue del microservicio o del proxy configurado. | Ver tarjetas, crear tarjeta, cambiar estado, eliminación, y errores controlados | Servicio `microservice-cards` (externo o proxificado) |

Se contempla la posibilidad de que se produzcan fallos: si un microservicio no está disponible, determinadas páginas pueden mostrar errores controlados o información estática, evitando bloqueos completos de la navegación. 

### Aspectos positivos del frontend
La arquitectura del frontend destaca por decisiones que facilitan el despliegue y la evaluación en entornos docentes:

* Separa la configuración de endpoints por variables de entorno, lo que permite cambiar entre despliegues sin modificar código. 
* Centraliza autenticación y sesión mediante token y almacenamiento local, reduciendo fricción en la navegación entre módulos. 
* Admite integración híbrida: parte del dominio se consume a través del API Gateway y parte directamente contra microservicios externos, lo que simplifica el montaje incremental del sistema
* Adaptación orientada a uso en escritorio y móvil (responsive), lo que mejora la accesibilidad de uso y la evaluación práctica en distintos dispositivos.

### 5.5 Frontend específico de cada microservicio

#### 5.5.1 Cards

Se ha implementado una página individual (BancUS-frontend/src/components/CardsPage.jsx) para la gestión de tarjetas, la cual realiza:
- Listado de tarjetas.
- Detalle de tarjeta.
- Alta de tarjeta.
- Edición de tarjeta.
- Eliminación de tarjeta.
- Congelar y reactivar tarjeta.
  
## 6. Descripción del API REST

### Microservicio Accounts (Python / Quart)
Desarrollado con `Quart` y `Quart-Schema` para soporte asíncrono y documentación automática.

**Prefijo:** `/v1/accounts`

| Método | Endpoint | Descripción | Códigos de Respuesta                                               |
| :--- | :--- | :--- |:-------------------------------------------------------------------|
| `POST` | `/` | Crea una nueva cuenta bancaria. | `201`, `400`                                                       |
| `GET` | `/` | Lista cuentas (paginado con `page`, `limit`). | `200`                                                              |
| `GET` | `/<iban>` | Obtiene detalles de una cuenta específica. | `200`, `400`, `404`                                                |
| `PATCH` | `/<iban>` | Actualiza datos parciales de la cuenta. | `200`, `400`, `404`                                                |
| `DELETE`| `/<iban>` | Elimina una cuenta. | `204`, `400`, `404`                                                |
| `PATCH` | `/operation/<iban>/<currency>` | Actualiza saldo con conversión de divisa. | `200`, `403` (Saldo insuf.), `503` (Error Microservico de divisas) |
| `PATCH` | `/<iban>/block` | Bloquea la cuenta (congela operaciones). | `204`, `400`, `404`                                                |
| `PATCH` | `/<iban>/unblock` | Desbloquea la cuenta. | `204`, `400`, `404`                                                |
| `POST` | `/card/<iban>` | Solicita creación de tarjeta asociada. | `200`, `404`, `503` (Error Cards)                                  |
| `DELETE`| `/card/<iban>` | Elimina tarjeta asociada. | `200`, `404`, `503` (Error Cards)                                  |

### Microservicio Cards (Node.js / Express)
Desarrollado con `Express` y persistencia en `MongoDB` (modelo `Card`). Incluye documentación **Swagger/OpenAPI** y una capa de caché (Redis) para acelerar operaciones de lectura. 

**Prefijo:** `/v1/cards` 

#### Modelo de datos (resumen)
La entidad `Card` almacenalos siguientes campos: `_id` (MongoDB), `card_id` (identificador del número de tarjeta por titular), `cardholderName` (nombre del propietario de la tarjeta), `PAN` (único), `expirationDate` (Fecha de expiración de la tarjeta), `CVC` (Código de seguridad) y `cardFreeze` (`Active`/`Frozen`). 

En la creación de tarjeta, el único campo requerido de entrada es `cardholderName`. `PAN`, `CVC` y `expirationDate` se generan automáticamente, siendo PAN un identificador único de 16 dígitos, CVC un número de 3 cifras aleatorio y expirationDate la fecha tres años posterior de la de la creación de la tarjeta.

| Método | Endpoint | Descripción | Códigos de Respuesta |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Lista **todas** las tarjetas. | `200`, `500` |
| `GET` | `/holder/<cardholderName>` | Lista todas las tarjetas de un titular por nombre. | `200`, `404` (sin tarjetas), `500`  |
| `GET` | `/<id>` | Obtiene una tarjeta por su id global (MongoDB). | `200`, `404`, `500` |
| `POST` | `/` | Crea una tarjeta para un usuario. Solo requiere `cardholderName`. El resto se genera automáticamente. | `201`, `400`, `500` :contentReference[oaicite:7]{index=7} |
| `PUT` | `/status/<id>/<cardFreeze>` | Bloquea o desbloquea una tarjeta por id (cambia `cardFreeze` a `Active`/`Frozen`). | `200`, `400` (estado inválido), `404`, `500` |
| `PUT` | `/<cardholderName>/<id>` | Actualiza una tarjeta por titular + id. Puede modificar `cardFreeze` y campos numéricos. | `200`, `400`, `404`, `500` |
| `PUT` | `/<id>` | Actualiza una tarjeta por id global. Puede modificar `cardFreeze` y campos numéricos. | `200`, `400`, `404`, `500` :contentReference[oaicite:10]{index=10} |
| `DELETE` | `/pan/<PAN>` | Elimina una tarjeta por su `PAN`. | `200`, `404`, `500` :contentReference[oaicite:11]{index=11} |
| `DELETE` | `/<cardholderName>/<id>` | Elimina una tarjeta por titular + id. | `200`, `404`, `500` :contentReference[oaicite:12]{index=12} |
| `DELETE` | `/<id>` | Elimina una tarjeta por id global. | `200`, `404`, `500` :contentReference[oaicite:13]{index=13} |

> Nota técnica: en operaciones que modifican estado o datos (POST/PUT/DELETE), se invalidan claves de caché relacionadas (por ejemplo, listados globales y por titular) para mantener consistencia. :contentReference[oaicite:14]{index=14}
> 
### Microservicio Currencies (Java / Spring Boot)
Desarrollado con Spring Boot.
**Prefijo:** `/v1/currency`

| Método | Endpoint | Parámetros (Query) | Descripción |
| :--- | :--- | :--- | :--- |
| `GET` | `/convert` | `from`, `to`, `amount` | Realiza la conversión de divisas utilizando el valor actual de mercado. |


---

## 6. Justificación de Requisitos y Evidencias

A continuación se detalla cómo se han implementado los patrones de arquitectura y requisitos técnicos exigidos, detallando la ubicación en el código fuente.

### 6.1. Resiliencia y Tolerancia a Fallos (Patrón Circuit Breaker & Fallbacks)
Para evitar fallos en cascada cuando un microservicio dependiente (Cards o Currencies) cae, se han implementado mecanismos de protección robustos.

* **Implementación (Accounts):** Se ha aplicado el **Patrón Circuit Breaker**. Si el microservicio de Divisas falla repetidamente, el sistema deja de enviar peticiones temporalmente y devuelve un error controlado, permitiendo que el servicio externo se recupere.
* **Gestión de Conexiones (Network Watcher):** Se ha desarrollado un *Network Watcher* que monitoriza los servicios externos (cache redis y base de datos) para comporbar su estado. Si se pierde la conexion con alguno, el sistema intenta reconectar. En el caso de la base de datos principal, se intenta reconectar 5 veces antes de que caiga el microservicio.
* **Evidencia en código:** [Ver implementación del Circuit Breaker / Network Watcher]([PON_AQUI_EL_LINK_A_GITHUB])

### 6.2. Estrategia de Caché Multinivel (Rendimiento y Costes)
Se ha implementado una estrategia de caché híbrida para reducir la latencia y, crucialmente, minimizar el consumo de APIs externas de pago.

* **Caché Distribuida (Redis):**  microservicios (Accounts, cards y Currencies) utilizan Redis como primera capa de caché para datos de acceso frecuente.
* **Caché Local (Fallback):** En el microservicio de **Accounts** y **Currencies**, se ha implementado un sistema de alta disponibilidad: si Redis se cae, el sistema conmuta automáticamente a una caché en memoria local del contenedor, garantizando que el servicio no se detenga por un fallo en la infraestructura de caché. Esto incrementaria el uso de recursos y la api externa ya que cada contenedor debe gestionar su propia cache.
* **Evidencia en código:** [Ver lógica de caché Redis/Local en Accounts]([PON_AQUI_EL_LINK_A_GITHUB])

### 6.3. Optimización de Recursos Externos (Gestión de Cuotas API)
El microservicio de **Currencies** consume la API externa "Currency Converter Pro1" de RapidAPI. Dado que el plan gratuito tiene un límite de 3000 peticiones/mes, se ha diseñado una lógica de ahorro estricta.

* 3000 peticiones mes equivalen aprox. a una petición cada 15-20 minutos. El sistema cachea los valores de las divisas en Redis con un TTL (Time To Live) ajustado a este intervalo. Si se solicita un cambio de divisa (ej. EUR -> USD) y el dato en caché es reciente, **no se consume cuota de la API externa**.
* **Evidencia en código:** [Ver servicio de Currencies y configuración de TTL]([PON_AQUI_EL_LINK_A_GITHUB_JAVA])

### 6.4. Observabilidad y Monitorización (Health Checks & Logs)
Para facilitar el despliegue en orquestadores como Kubernetes y la depuración, se han estandarizado los mecanismos de salud y trazas.

* **Health Checks (Kubernetes Ready):**
    * **Accounts:** Endpoint específico `/health` diseñado para los *liveness probes* de Kubernetes.
    * **Cards:** Endpoint específico `/health` diseñado para los *liveness probes* de Kubernetes.
    * **Currencies:** Uso de **Spring Boot Actuator** para exponer métricas y estado de salud estándar.
* **Sistema de Logs:** Los microservicios Accounts y Cards implementan un sistema de logs estructurado que permite rastrear el flujo de las peticiones y los errores internos. Este sistema de logs vuelca los logs a salida estandar para luego poder caputrarlos con grafana en kubernetes (sistema de logs centralizado)
* **Evidencia en código:** [Ver endpoint de Health en Accounts]([PON_AQUI_EL_LINK_A_GITHUB])

### 6.5. Documentación Viva (OpenAPI/Swagger)
La documentación de la API se mantiene siempre sincronizada con el código gracias a la generación automática.

* En el microservicio de Accounts, se utiliza la integración de `quart-schema`. Esto expone automáticamente un `schema.json` y una interfaz Swagger UI basada en los modelos Pydantic y los decoradores de las rutas, asegurando que la documentación nunca quede obsoleta frente al código. Lo mismo ocurre en spring boot con su equivalente.
* **Evidencia en código:** [Ver configuración de Quart-Schema en app.py]([PON_AQUI_EL_LINK_A_GITHUB])

La documentación del microservicio Cards se mantiene sincronizada con el código mediante generación automática de la especificación OpenAPI a partir de anotaciones en las rutas.

En este microservicio se emplea swagger-jsdoc para generar dinámicamente el documento OpenAPI 3.0 (swaggerSpec) en tiempo de arranque. La fuente de verdad de la documentación no es un fichero OpenAPI escrito a mano, sino las anotaciones JSDoc incluidas en el propio fichero de rutas (./routes/cards.js), indicado explícitamente en swaggerOptions.apis. De este modo, cualquier cambio en los endpoints o en sus contratos, queda incorporado automáticamente en la especificación generada.

A continuación, swagger-ui-express publica una interfaz Swagger UI montada en la ruta /api-docs, sirviendo el swaggerSpec generado por swagger-jsdoc. Esto convierte la documentación en “viva”, accesible desde el propio servicio y alineada con el estado del código.

* **Evidencia en código:** [Ver anotaciones swagger microservice-cards]([https://github.com/BancUS-FISProject/microservice-cards/blob/master/routes/cards.js])
---

### 6.6. Seguridad y Control de Acceso (CORS, Auth y cabeceras)

Se ha incorporado una configuración explícita de CORS en el microservicio de Cards para permitir el consumo desde el frontend, restringiendo origen, métodos y cabeceras permitidas. Esto evita bloqueos por política del navegador y reduce exposición innecesaria a orígenes no autorizados.

Adicionalmente, se realiza una propagación de credenciales en cabecera `Authorization: Bearer <token>` cuando el sistema opera con autenticación, así como la coherencia de los códigos `401/403` definidos en el SLA.

* **Evidencia en código:** [Ver configuración CORS en app.js]([PON_AQUI_EL_LINK_A_GITHUB])
* **Evidencia en código:** [Ver uso de Authorization en el cliente del frontend]([PON_AQUI_EL_LINK_A_GITHUB])

### 6.7. Consistencia de Caché e Invalidación (Cards)

Se utiliza Redis como caché para reducir latencia en lecturas frecuentes (por ejemplo, listados y consultas por titular). Para evitar inconsistencias, tras operaciones de escritura (POST/PUT/DELETE) se invalidan las claves relacionadas o se actualizan entradas puntuales, garantizando que el frontend no consuma información obsoleta.

Además, se incluye un endpoint simple de verificación (`/ping/cache`) para facilitar pruebas de integración desde frontend y test externos.

* **Evidencia en código:** [Ver inicialización Redis y uso de caché]([PON_AQUI_EL_LINK_A_GITHUB])
* **Evidencia en código:** [Ver endpoint /ping/cache]([PON_AQUI_EL_LINK_A_GITHUB])

### 6.8. Observabilidad: Request ID, logs estructurados y trazabilidad

El microservicio Cards incorpora un middleware que asigna o propaga un `x-request-id` por petición, midiendo latencia y registrando método, ruta y código de respuesta con logs estructurados. Esta práctica permite correlacionar llamadas desde el gateway y depurar incidencias en entornos distribuidos.

* **Evidencia en código:** [Ver middleware x-request-id y logging en app.js]([PON_AQUI_EL_LINK_A_GITHUB])


## 7. Análisis de Esfuerzos

Se ha realizado un seguimiento de las horas dedicadas mediante herramienta de Time Tracking.

| Tarea / Módulo                          | Horas Aprox. |
|:----------------------------------------| :--- |
| Diseño de Arquitectura y API Gateway    | XX h |
| Microservicio Accounts (Python) y Tests | XX h |
| Microservicio Currencies (Java)         | XX h |
| Documentación y Despliegue              | XX h |
| **TOTAL**                               | **XX Horas** |

![Gráfico de Esfuerzo](https://via.placeholder.com/600x300?text=Pegar+Captura+Clockify/Toggl+Aqui)

---

## 8. Uso de Inteligencia Artificial

Para el desarrollo de este proyecto se ha utilizado IA generativa (ChatGPT/GitHub Copilot) como herramienta de soporte en los siguientes aspectos:

1.  **Traducción de Lógica a Java Spring Boot:** Apoyo para generar la estructura sintáctica correcta del `RestController` y la inyección de dependencias en Java, agilizando el cambio de contexto desde Python.
2.  **Manejo de Asincronía en Python:** Consultas sobre el uso correcto de `async/await` en los Blueprints de Quart para asegurar que no se bloqueara el event loop.
3.  **Documentación de API:** Generación de plantillas para la documentación de los endpoints basadas en los decoradores de código.
4.  **Depuración de Errores HTTP:** Ayuda para entender mejor los códigos de estado HTTP correctos para situaciones específicas (diferencia entre 403 Forbidden y 400 Bad Request en lógica de negocio bancaria).
5.  **Depuración de errores CSS:** apoyo para identificar y corregir problemas de maquetación y estilos en el frontend, incluyendo ajustes de diseño responsive, alineación de componentes, gestión de desbordamientos, y coherencia visual entre vistas públicas (sin sesión) y privadas (con sesión), asegurando una experiencia de usuario estable en distintos tamaños de pantalla.
