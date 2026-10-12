# HILOS — Propuesta de sistema (v0.1)

Borrador para afinar con Gerencia General. 12 de octubre de 2026.

Marcas usadas en el documento: **[H]** hecho verificado, **[S]** supuesto o estimación por validar.

---

## 1. Problema y objetivo

La Gerencia General pierde el hilo de lo conversado durante la semana con sus cuatro reportes directos y, en consecuencia, falla el seguimiento de temas estratégicos y operativos. Planner no logró adopción: exige documentar a mano y la vista no ayuda a leer el estado de las cosas.

HILOS debe:

1. Mantener, por cada reporte directo, la lista viva de temas abiertos con su estado de decisión, su nivel de implementación y su resultado.
2. Alimentarse sola de las comunicaciones diarias (correo primero, Slack después) y permitir la captura manual.
3. Mantener visible cada tema hasta su cierre formal.
4. Empezar con la Gerencia General, extenderse a los cuatro reportes y luego al resto de la organización (incluida la eventual sustitución de Asana en Mercadeo).
5. Reducir la dependencia operativa de la Gerencia General. Si un diseño exige su supervisión permanente para funcionar, es un mal diseño.

## 2. Hallazgos que condicionan el diseño

Revisión de una semana de correo y calendario (5 al 12 de octubre de 2026) y de los permisos del conector de Microsoft 365:

| # | Hallazgo | Implicación para el diseño |
|---|---|---|
| 1 | **[H]** Los 1:1 son presenciales ("Oficina Jeremy"), los lunes a las 2:00, 3:00 y 4:00 p.m. (Comercial, Operaciones, RRHH). | Los acuerdos más importantes de la semana se toman fuera del correo. |
| 2 | **[H]** Hay correos posteriores que citan acuerdos del 1:1 de memoria ("en los acuerdos de la semana pasada en el 1:1 quedamos que…"), con versiones que no coinciden. | Si HILOS lee solo el correo, pierde la fuente principal. El 1:1 tiene que ser una fuente de primer nivel (§4.5). |
| 3 | **[H]** No aparece en el calendario un 1:1 recurrente con la Asistente Contable. | Confirmar si existe y por qué canal se hace el seguimiento con ella. |
| 4 | **[H]** RRHH opera con un buzón de rol (`recursoshumanos@`). | Los temas se asignan a un **rol** además de a una persona; si la persona cambia, el rol conserva su historial. |
| 5 | **[H]** El buzón de la Gerencia mezcla temas operativos con temas legales y patrimoniales (ya existe la categoría de Outlook "P2 - Legal y patrimonial"). | Las reglas de exclusión son obligatorias desde el primer día (§4.10). |
| 6 | **[H]** El conector de Microsoft 365 disponible en Claude es de solo lectura (correo, calendario, Teams, transcripciones de reuniones de Teams). No tiene permisos sobre Planner ni para enviar correo. | Sirve para el prototipo (Fase 0). Producción necesita su propia aplicación registrada en el Entra ID de HR Suplidora. |
| 7 | **[H]** En Entra ID, el cargo de la cuenta de la Gerencia General figura como "Gerente Comercial". | Corregirlo si HILOS va a usar el directorio para asignar roles. |

## 3. Concepto central

### 3.1 La unidad: el Hilo

Un **Hilo** es un tema que requiere seguimiento, desde que aparece hasta que se cierra. Tipos:

- **Decisión**: alguien tiene que escoger entre opciones.
- **Acción**: alguien tiene que ejecutar algo concreto.
- **Proyecto**: acción de largo aliento con hitos (puede tener subhilos).
- **Idea**: tema sin compromiso todavía; puede convertirse en decisión o acción.
- **Seguimiento de indicador**: KPI u OKR que se revisa en el 1:1.
- **Riesgo / problema**: algo que puede salir mal o ya salió mal.

### 3.2 Ciclo de vida (tres ejes independientes)

**Eje 1. Decisión**

| Estado | Significado |
|---|---|
| Por decidir: Gerencia General | La pelota está en la cancha de la Gerencia. |
| Por decidir: responsable | La pelota está en la cancha del reporte. |
| Por decidir: tercero | Proveedor, abogado, contador, cliente. |
| Decidido | Hay decisión, con fecha y evidencia. |
| No requiere decisión | Acciones que ya vienen definidas. |

**Eje 2. Nivel de implementación** (los cuatro estados solicitados, más dos de cierre o excepción)

`Sin iniciar` → `En proceso` → `En revisión` → `Completada`, más `En pausa / bloqueado` y `Descartado`.

**Eje 3. Resultado** (solo cuando la implementación está completada)

`Sin medir` · `Logrado` · `Parcial` · `No logrado`, con el dato que lo sustenta.

**Regla de visibilidad:** un hilo aparece en el reporte de su responsable hasta que esté `Completada` con resultado registrado, o `Descartado`. Se muestra una vez en "Cerrados esta semana" y luego pasa al archivo, donde se puede consultar.

### 3.3 Evidencia obligatoria

Todo cambio de estado lleva su fuente: cita textual, enlace al correo o mensaje original, fecha y quién lo confirmó. Si la IA no encuentra evidencia suficiente, el campo queda como "por confirmar"; nunca se rellena por inferencia.

## 4. Características y capacidades

### 4.1 Ingesta automática

- **Correo (Outlook)**: lectura incremental cada 15 minutos de los hilos de correo donde participen la Gerencia General y al menos uno de los reportes directos. En Fase 2 se suman los buzones de los reportes con sus equipos.
- **Slack**: canales y mensajes directos autorizados (Fase 2).
- **Calendario**: detecta los 1:1 y otras reuniones para anclar la agenda y los acuerdos.
- **Transcripciones de Teams** (opcional): si un 1:1 se registra como reunión de Teams con transcripción activada, aunque sea presencial, HILOS puede extraer los acuerdos directamente.
- **Adjuntos** (Fase 2+): texto de PDF y Excel cuando el contenido del tema esté ahí.

### 4.2 Motor de IA

Para cada mensaje nuevo, el motor:

1. Decide si toca un hilo existente, si crea uno nuevo o si es ruido (saludos, avisos automáticos).
2. Extrae: decisión tomada o solicitada (y de quién), compromiso, responsable, fecha comprometida, cambio de estado y resultado reportado.
3. Empareja contra los hilos abiertos con búsqueda semántica, para no duplicar temas que se escribieron con otras palabras.
4. Produce una **propuesta** con nivel de confianza y la cita que la justifica.
5. Aprende de las correcciones: cada corrección queda como ejemplo para la siguiente vez, junto con un glosario de personas, apodos, códigos de producto y siglas internas.

Niveles de autonomía configurables:

| Tipo de cambio | Fase 0–1 | Fase 2+ (si la precisión lo justifica) |
|---|---|---|
| Hilo nuevo | Requiere confirmación | Requiere confirmación |
| Actualización de estado con evidencia explícita | Requiere confirmación | Se aplica sola y se notifica |
| Cierre / descarte | Requiere confirmación | Requiere confirmación |

### 4.3 Bandeja de propuestas

Una sola vista donde se confirman, corrigen o rechazan en lote las propuestas de la IA. Meta de uso: menos de 10 minutos por semana **[S]**. En Fase 2 cada reporte confirma las propuestas de sus propios hilos, de modo que la Gerencia deja de ser el cuello de botella.

### 4.4 Reporte 1:1 por reporte directo

Se genera el domingo en la noche y se entrega el lunes temprano (web y correo). Secciones:

1. **Requiere tu decisión**: lo que espera de la Gerencia General, con días de espera.
2. **Requiere decisión de [persona]**.
3. **Novedades de la semana**: cambios de estado, con evidencia.
4. **En ejecución**: mediano y largo plazo, con nivel de implementación, fecha y semáforo.
5. **Alertas**: vencidos, sin movimiento por más de 14 días, compromisos sin fecha o sin responsable, versiones contradictorias de un mismo acuerdo.
6. **Resultados por medir**: lo implementado que aún no tiene resultado registrado.
7. **Temas nuevos detectados**: por confirmar.
8. **Cerrados esta semana**.
9. **Preguntas sugeridas para el 1:1**.

### 4.5 Modo 1:1 en vivo y acta

- Durante el 1:1, la agenda se abre en pantalla (computadora o tablet) y cada acuerdo se marca con un toque: decidido, responsable, fecha.
- Al cerrar, HILOS genera el **acta** y la envía por correo al reporte. El acta es la versión oficial del acuerdo y alimenta de vuelta al sistema.
- Alternativa sin pantalla: nota de voz o transcripción de Teams que la IA convierte en propuestas.

### 4.6 Captura manual

- Botón "+ Hilo" en web y móvil (instalable como app, PWA).
- Reenviar un correo a `hilos@hrsuplidora.com` con una nota: crea una propuesta.
- En Slack: comando `/hilo` o reacción 🧵 sobre un mensaje (Fase 2).

### 4.7 Vistas

- **Por persona**: el reporte 1:1 vivo.
- **Lo que espera de mí**: todas las decisiones pendientes de la Gerencia General.
- **Tablero**: columnas por nivel de implementación, con filtros por área, tipo y horizonte.
- **Línea de tiempo**: hilos de mediano y largo plazo con hitos.
- **OKR 2026**: hilos vinculados a cada objetivo y resultado clave.
- **Archivo**: búsqueda en todo lo cerrado, con su historia.

### 4.8 Termómetro de delegación

Indicadores semanales:

- Decisiones pendientes de la Gerencia General (cantidad y días promedio de espera).
- Porcentaje de hilos que el equipo cerró sin intervención de la Gerencia.
- Porcentaje de hilos con responsable distinto de la Gerencia General.
- Temas que se escalaron a la Gerencia y que pudieron resolverse en el área.

Si la delegación avanza, la primera línea baja y las otras suben.

### 4.9 Notificaciones

- Lunes 6:30 a.m.: reportes 1:1.
- Recordatorio a cada responsable: compromisos que vencen esa semana.
- Resumen diario: en Fase 1 HILOS absorbe el resumen diario que hoy corre en Zapier, para no tener dos pipelines de IA leyendo el mismo buzón.

### 4.10 Permisos, confidencialidad y exclusiones

- Inicio de sesión con la cuenta de Microsoft 365 de HR Suplidora (SSO).
- La Gerencia General ve todo. Cada reporte ve sus hilos y los de su equipo. Seguridad aplicada a nivel de fila en la base de datos, no solo en pantalla.
- **Nunca se ingieren**: correos con la categoría "P2 - Legal y patrimonial" (o la que se defina), hilos solo con externos sin participación de un reporte y remitentes en lista de exclusión (abogados, bancos, contador externo, temas familiares).
- Hilos marcados como **confidenciales** (salarios, disciplinarios, salud): visibles solo para las personas autorizadas, incluso si el sistema se extiende a toda la organización.
- Bitácora inmutable de quién cambió qué y cuándo.

### 4.11 Escalabilidad organizacional (Fase 3)

- Espacios por área: Gerencia, Comercial, Mercadeo, Operaciones, RRHH, Contabilidad.
- Subhilos, dependencias, plantillas (por ejemplo, "lanzamiento de producto", "importación China"), tareas recurrentes, comentarios con @menciones y adjuntos enlazados a SharePoint.
- Sustitución de Asana en Mercadeo: solo después de comparar con datos (uso real, costo de licencias, flujo creativo de aprobaciones). No es un objetivo en sí mismo.
- Integración posterior con SAP B1 para registrar resultados con datos duros (por ejemplo, ventas de un lanzamiento).

### 4.12 Requisitos no funcionales

Interfaz en español, zona horaria de Costa Rica, uso cómodo en celular, exportación a Excel, respaldos diarios, tope de gasto mensual en IA con alerta y datos portables (base de datos estándar exportable, sin dependencia de un proveedor cerrado).

## 5. Modelo de datos (borrador)

| Entidad | Campos principales |
|---|---|
| **Rol** | nombre (Gerencia Comercial…), área, persona actual, buzón(es) |
| **Persona** | nombre, correo(s), usuario de Slack, rol |
| **Hilo** | título, descripción, tipo, área, rol responsable, persona responsable, contraparte, prioridad (P1–P3), horizonte (corto ≤2 semanas, mediano ≤3 meses, largo >3 meses), OKR vinculado, fecha compromiso, estado de decisión, nivel de implementación, resultado, confidencialidad, hilo padre |
| **Evento** | hilo, fecha, fuente (correo, Slack, 1:1, manual), cita, enlace al original, cambio aplicado, confianza, confirmado por |
| **Propuesta** | evento candidato, estado (pendiente, aceptada, corregida, rechazada), corrección |
| **Reunión 1:1** | fecha, rol, agenda generada, acta, acuerdos (eventos) |
| **Mensaje fuente** | id externo, canal, remitente, fecha, procesado, excluido (y por qué) |

## 6. Arquitectura y herramientas

### 6.1 Recomendación

| Capa | Herramienta | Por qué |
|---|---|---|
| Frontend | **Next.js + TypeScript + Tailwind + shadcn/ui**, instalable como PWA | Estándar de mercado, buena experiencia móvil, fácil de mantener por cualquier desarrollador o por Claude Code. |
| Hosting frontend | **Vercel** | Vista previa automática de cada cambio antes de publicarlo: la Gerencia revisa desde el celular y aprueba. |
| Backend y base de datos | **Supabase** (PostgreSQL, autenticación con Microsoft Entra, seguridad por fila, almacenamiento, funciones programadas, colas, búsqueda semántica con pgvector) | Un solo servicio administrado cubre base de datos, permisos, tareas programadas y búsqueda semántica. Es PostgreSQL estándar: los datos son portables. |
| Ingesta de correo | **Microsoft Graph API** con una aplicación registrada en el Entra ID de HR Suplidora, con permiso de lectura limitado a los buzones autorizados (RBAC para aplicaciones de Exchange Online) | Acceso de producción independiente de cualquier cuenta personal. |
| Ingesta de Slack | Bot de Slack en el workspace de HR Suplidora | Lectura de canales autorizados y comando `/hilo`. |
| IA | **Claude API**: Claude Opus 5.5 para extracción y síntesis semanal; evaluar con datos un filtro previo con Claude Haiku 5.5. Batch API (−50%) para lo que no es urgente y caché de prompts. | Calidad de extracción en español con evidencia citada. |
| Envío de correo | Microsoft Graph desde el buzón `hilos@hrsuplidora.com` | Las actas y los reportes salen del dominio de la empresa. |
| Código y despliegue | **GitHub** (este repositorio) + GitHub Actions | Historial completo, revisión de cambios y despliegue automático. |

### 6.2 Flujo

```
Outlook / Slack / 1:1 / manual
        │ (cada 15 min, lectura incremental)
        ▼
Exclusiones ──► descartados (con razón registrada)
        │
        ▼
Motor IA (Claude API) ──► Propuestas con evidencia
        │                         │
        │                 Bandeja de confirmación
        ▼                         │
     Hilos + Eventos (Supabase) ◄─┘
        │
        ├──► Vistas web/móvil (Vercel)
        ├──► Reporte 1:1 (domingo noche) ──► correo lunes 6:30 a.m.
        └──► Acta post-1:1 ──► correo al reporte ──► vuelve a la ingesta
```

### 6.3 Alternativas evaluadas

| Opción | Ventaja | Por qué no como base |
|---|---|---|
| Ecosistema Microsoft (Planner Premium o Listas + Power Automate + Copilot Studio) | Todo queda dentro del tenant y el equipo ya usa Microsoft 365. | Se mantiene la misma experiencia visual que ya no funcionó. Power Automate se vuelve frágil con lógica compleja y el licenciamiento premium es por usuario. |
| Knack (ya conectado a Claude) | No-code, rápido para prototipar formularios y tablas. | Débil para tableros, agenda de 1:1 y lógica de IA; el motor tendría que vivir fuera de todas formas. Además, hoy se usa para otro proyecto; conviene mantener separadas las plataformas de cada empresa. |
| Asana, ClickUp o Notion con IA | Producto maduro, sin desarrollo. | Ninguno se alimenta del correo con trazabilidad de decisiones. Licencias por usuario y datos en un sistema cerrado. |
| Desarrollo en Azure (Functions + SQL + Static Web Apps) | Datos dentro del ecosistema Microsoft. | Más operación y más costo de mantenimiento para una PYME. Solo se justifica si se exige que todo viva en el tenant. |

## 7. Costos estimados **[S]**

Tipo de cambio de referencia: ₡507 por USD.

| Rubro | USD/mes | CRC/mes | Nota |
|---|---|---|---|
| Claude API, Fase 1 (~1.000–1.500 correos/mes) | 25–100 | ₡12.700–50.700 | El extremo bajo asume Batch API y filtro previo; el alto, todo con Opus 5.5 sin optimizar. Precios vigentes a octubre de 2026: Opus 5.5 USD 4 / 20, Haiku 5.5 USD 0,10 / 0,50 por millón de tokens de entrada / salida. |
| Supabase (plan Pro) | ~25 | ~₡12.700 | Precio público de referencia; verificar. |
| Vercel (plan Pro, 1 usuario) | ~20 | ~₡10.100 | Precio público de referencia; verificar. El plan gratuito no permite uso comercial. |
| **Total Fase 1** | **~70–145** | **~₡35.500–73.500** | |
| Fase 2–3 (5+ buzones) | 150–350 | ₡76.000–177.000 | El costo de IA crece con el volumen de mensajes, no con los usuarios. |

No incluye el tiempo de la Gerencia General ni la suscripción de Claude que se usa para desarrollar, que ya existe.

## 8. Fases

| Fase | Duración **[S]** | Alcance | Criterio de salida |
|---|---|---|---|
| **0. Prototipo sin software** | 3 semanas | Rutina programada de Claude que el domingo en la noche lee los correos de la semana con cada reporte (conector actual de Microsoft 365), mantiene el estado de los hilos y publica una página privada con los cuatro reportes 1:1. La Gerencia corrige y las correcciones alimentan la siguiente corrida. | Al menos 80% de los hilos detectados son correctos según la Gerencia y la corrección toma menos de 15 minutos por semana. Taxonomía y estados validados. |
| **1. MVP para la Gerencia** | 5–6 semanas | Aplicación web: ingesta automática, bandeja de propuestas, reporte 1:1, modo en vivo y acta, captura manual, exclusiones, absorción del resumen diario de Zapier. | Cuatro 1:1 consecutivos dirigidos desde HILOS. Planner deja de usarse para este fin. |
| **2. Apertura a los reportes** | 6–8 semanas | Acceso de los cuatro reportes, confirmación de sus propios hilos, Slack, sus buzones, política de uso comunicada al personal. | Cada reporte mantiene sus hilos sin intervención de la Gerencia; el termómetro de delegación mejora. |
| **3. Escalamiento organizacional** | Por definir con datos | Espacios por área, proyectos y plantillas, evaluación de reemplazo de Asana, integración con SAP B1. | Decisión documentada para cada herramienta que se sustituya. |

## 9. Gestión del proyecto con Claude en la nube

### 9.1 Separación de papeles

- **Gerencia General = dueño de producto** en Fases 0–1: define qué se construye, prioriza y aprueba. Desde la Fase 2 se designa un **dueño funcional interno** para el día a día.
- **Claude Code en la nube = equipo de desarrollo**: diseña, programa, prueba, documenta y mantiene. Cada sesión trabaja en un contenedor aislado sobre este repositorio.
- **Claude API dentro de HILOS = motor de producción**. El sistema en operación **no depende** de sesiones de Claude Code ni de la cuenta personal de nadie: corre con sus propias credenciales, contratadas a nombre de quien sea dueño del sistema (ver §10).

### 9.2 Repositorio como fuente de verdad

- `CLAUDE.md`: contexto del negocio, convenciones y reglas (no inventar datos, español costarricense, evidencia obligatoria).
- `docs/`: esta propuesta, decisiones de arquitectura (una por archivo, con su razón) y glosario.
- Backlog en GitHub Issues, con un hito por fase.

### 9.3 Ciclo de cada cambio

1. La Gerencia describe la necesidad en español, desde la app de Claude (también desde el celular).
2. Claude crea una rama, implementa, corre las pruebas y abre un pull request.
3. Vercel genera una vista previa; la Gerencia la revisa desde el celular.
4. Con la aprobación, se fusiona y se publica automáticamente.
5. Claude vigila el pull request (pruebas, comentarios) hasta que queda limpio.

### 9.4 Entorno en la nube

- **Secretos** (llaves de Supabase de desarrollo, Claude API de desarrollo): se guardan en la configuración del entorno, nunca en el repositorio ni en el chat.
- **Red**: se habilitan solo los dominios necesarios (Supabase, Vercel, Anthropic, Microsoft Graph). Referencia: https://code.claude.com/docs/en/cloud-environments#network-access
- **Script de inicio**: instala dependencias y corre pruebas al abrir cada sesión.
- **Dos ambientes**: Claude Code trabaja contra un proyecto de **desarrollo** con datos de prueba. Las credenciales de producción (buzones reales) viven solo en Vercel y Supabase de producción, nunca en una sesión de desarrollo.

### 9.5 Rutinas programadas

- **Fase 0**: la rutina semanal que genera los reportes 1:1.
- **Desde la Fase 1**: una rutina semanal de "salud del sistema" (costo de IA, errores de ingesta, precisión medida por las correcciones) con un informe corto a la Gerencia.

### 9.6 Calidad de la IA

Las correcciones de la Fase 0 se convierten en un **set de evaluación**: un grupo de correos reales con la respuesta correcta. Ningún cambio en las instrucciones del motor se publica sin superar ese set.

### 9.7 Dedicación estimada de la Gerencia General **[S]**

Fases 0–1: una sesión semanal de 30–45 minutos para revisar y decidir, más la corrección semanal de propuestas. Fase 2 en adelante: revisión quincenal; el dueño funcional asume el resto.

## 10. Riesgos y mitigación

| Riesgo | Mitigación |
|---|---|
| **Propiedad del sistema y de los datos.** El repositorio está en la cuenta personal de GitHub y el desarrollo se hace con una cuenta personal de Claude; los datos procesados son de HR Suplidora. | Definir con el abogado quién es dueño del código (HR Suplidora, la Gerencia General a título personal o una sociedad que lo licencie) **antes** de la Fase 1, y contratar los servicios de producción a nombre de ese titular. |
| **Datos personales.** Correos de colaboradores y clientes procesados por terceros en la nube (Ley 8968 de Protección de la Persona frente al Tratamiento de sus Datos Personales). | Validar con el abogado; política de uso comunicada al personal antes de la Fase 2; exclusiones y retención limitada (solo extractos y enlaces, no copias completas de los correos). |
| **Dependencia de la Gerencia** como dueña del producto. | Dueño funcional interno desde la Fase 2; documentación en el repositorio; stack estándar mantenible por cualquier desarrollador. |
| **Errores de la IA** (temas inventados o estados mal leídos). | Evidencia obligatoria, confirmación humana, set de evaluación y métricas de precisión. |
| **Baja adopción** de los reportes, como pasó con Planner. | Fase 2 solo después de que la Gerencia lo use cuatro semanas; los reportes reciben valor (actas claras, menos preguntas repetidas) antes de que se les pida esfuerzo. |
| **Costo de IA** creciente. | Tope mensual con alerta, Batch API, caché de prompts y filtro previo si los datos lo respaldan. |

## 11. Decisiones pendientes para cerrar el requerimiento

1. Titularidad del código, de las cuentas de nube y de los datos (consulta con el abogado).
2. Fuente del 1:1: captura en vivo en pantalla, transcripción de Teams o ambas.
3. Exclusiones: categorías, remitentes y temas que nunca entran.
4. Aceptación de los estados adicionales `En pausa / bloqueado` y `Descartado`.
5. 1:1 con la Asistente Contable: frecuencia y correo.
6. Aprobación del stack (§6.1) o preferencia por mantener todo dentro de Microsoft.
7. Arranque de la Fase 0.
