# HILOS — Propuesta de sistema (v0.2)

Borrador para afinar con la Gerencia General. 12 de octubre de 2026.

Marcas usadas en el documento: **[H]** hecho verificado, **[S]** supuesto o estimación por validar, **[D]** decisión tomada por la Gerencia General.

## Cambios respecto a la v0.1

- La publicación de seguimiento sale todos los lunes a las 6:45 a.m. y no depende del calendario. **[D]**
- Todo se asigna a **puestos**, no a personas. La estructura se toma del perfil de Microsoft Entra ID. **[D]**
- Se aceptan los estados `En pausa` y `Descartado`. **[D]**
- Solo entran conversaciones internas: correo @hrsuplidora.com y el Slack de HR Suplidora. Lo que venga de terceros externos se agrega a mano. **[D]**
- Nuevo **borrador de tareas a agregar**: el usuario decide qué se convierte en hilo y qué se descarta. Los hilos se pueden editar. **[D]**
- Los 1:1 son presenciales y conversacionales. Al terminar, se envía un correo sencillo con los temas tratados y de ahí se cargan las tareas solas. **[D]**
- Agrupación por área y por proyecto, con subtareas, y evaluación de cumplimiento para medir el desempeño del ejecutor. **[D]**
- Nueva sección de seguridad (§6).
- Nueva sección de cuentas, accesos y continuidad (§8), con un modelo de acceso delegable.

---

## 1. Problema y objetivo

La Gerencia General pierde el hilo de lo conversado durante la semana con sus reportes directos y falla en el seguimiento de temas estratégicos y operativos. Planner no logró adopción.

HILOS debe:

1. Mantener, para cada puesto que reporta a la Gerencia General, la lista viva de temas abiertos con su estado de decisión, nivel de implementación y resultado.
2. Alimentarse de las conversaciones internas, con captura manual cuando haga falta.
3. Mantener visible cada tema hasta su cierre formal.
4. Empezar con la Gerencia General, extenderse a sus reportes y luego al resto de la organización, con la posibilidad de sustituir Asana en Mercadeo.
5. Funcionar sin depender de la presencia de la Gerencia General.

## 2. Concepto central

### 2.1 Hilo, tarea y subtarea

Un **Hilo** es un tema que requiere seguimiento. Tipos: decisión, tarea, proyecto, idea, seguimiento de indicador, riesgo o problema.

- Cada hilo pertenece a un **área**, la del puesto responsable por defecto, y opcionalmente a un **proyecto**. Un proyecto puede abarcar varias áreas.
- Un hilo pesado o de trabajo en equipo se divide en **subtareas**, cada una con su propio puesto responsable y su propia fecha. Arrancamos con un nivel (hilo → subtareas) y se amplía si hace falta.
- El avance del hilo padre muestra el porcentaje de subtareas completadas. El estado del padre lo decide su responsable.

### 2.2 Puestos, no personas **[D]**

- Los hilos se asignan a un **puesto** (por ejemplo, Gerencia Comercial). La persona que ocupa el puesto hoy se toma del directorio.
- Si alguien renuncia, sale o cambia de puesto, los hilos se quedan con el puesto y los ve quien llegue.
- Si el puesto queda vacante, sus hilos se muestran al superior del puesto, marcados como "puesto vacante".
- La **evaluación de desempeño sí es de la persona**: cada cierre guarda quién lo ejecutó en ese momento (§4.9).

**Fuente de la estructura: Microsoft Entra ID.** HILOS sincroniza cada día, por cada usuario:

| Campo de Entra | Uso en HILOS | Requisito |
|---|---|---|
| Cargo (`jobTitle`) | Puesto | Catálogo único de nombres de puesto, escritos siempre igual. |
| Departamento (`department`) | Área | Catálogo único de áreas. |
| Jefe directo (`manager`) | Superior; de ahí salen pares y reportes directos | Lleno en el 100% de los colaboradores. |
| Correo | Vínculo con correo y Slack | El correo de Slack debe coincidir con el de Microsoft. |
| Estado de la cuenta | Detectar salidas y vacantes | Desactivar la cuenta el día de la salida. |

**[H]** Hoy el cargo de la cuenta de la Gerencia General figura como "Gerente Comercial". No pude revisar el resto de perfiles porque el conector de Claude no tiene permiso para leer el directorio completo. La depuración de perfiles es una tarea previa a la Fase 1 que puede hacer RRHH junto con quien administre Microsoft 365.

**[H]** HR Suplidora ya trabaja con muchas cuentas de rol: `recursoshumanos@`, `gestion@`, `sig@`, `bodega@`, `produccion@`, `ventas4@`, `contabilidad@` y `asistente.mercadeo@`. Esto calza con el modelo por puesto. Cada cuenta de rol debe tener su cargo, área y jefe en Entra igual que una cuenta personal.

### 2.3 Ciclo de vida (tres ejes)

**Decisión:** por decidir (por la Gerencia General, por el responsable o por un tercero), decidido, no requiere decisión.

**Implementación:** `Sin iniciar` → `En proceso` → `En revisión` → `Completada`, más `En pausa` y `Descartado`. **[D]**

**Resultado:** cuando la implementación está completada, `Sin medir`, `Logrado`, `Parcial` o `No logrado`.

**Regla de visibilidad:** un hilo aparece en los seguimientos hasta que esté `Completada` con resultado, o `Descartado`. Luego pasa al archivo.

### 2.4 Evidencia

Todo hilo y todo cambio guarda su fuente: cita, enlace al correo o mensaje, fecha y quién lo confirmó. Si falta información, el campo queda "por confirmar". Nunca se rellena por inferencia.

## 3. Fuentes de información

### 3.1 Solo conversaciones internas **[D]**

| Fuente | Regla de entrada |
|---|---|
| Correo | Entra si el remitente y **todos** los destinatarios (Para y CC) son @hrsuplidora.com. Un correo externo reenviado de forma interna sí entra, porque el reenvío es una conversación interna. Quedan fuera las direcciones internas de sistemas o notificaciones automáticas (lista configurable). |
| Slack | Solo el workspace de HR Suplidora. Quedan fuera los canales compartidos con otras organizaciones (Slack Connect) y los usuarios invitados externos. |
| Externos | Si un tercero externo genera una tarea, se agrega manualmente (§4.4). |

Detalles de la lectura de correo:

- **[H]** El 74% del correo interno recibido en dos semanas estaba en *Elementos eliminados*. La ingesta lee todas las carpetas, incluida esa, y procesa cada correo cuando llega, antes de que se borre.
- Quedan fuera:
  - el resumen diario que la Gerencia se envía a sí misma (Zapier);
  - las notificaciones de sistemas internos, como las de gestión documental (`sgd@` y `documentos@`) o las de formularios;
  - las invitaciones y respuestas de calendario.
- Slack avisa a HILOS por eventos cuando hay un mensaje nuevo, así que no hay que consultarlo periódicamente.

Cobertura por fase:

| Fase | Cobertura |
|---|---|
| 0–1 | Conversaciones donde participa la Gerencia General. |
| 2 | Buzones y Slack de los puestos que reportan a la Gerencia. |
| 3 | Toda la organización. |

### 3.2 Lo que ya no se usa

No se usa el calendario. La publicación y las actas no dependen de que haya una reunión agendada. **[D]**

## 4. Capacidades

### 4.1 Motor de IA

Para cada conversación interna nueva, el motor:

1. Decide si toca un hilo existente, si propone uno nuevo o si es ruido.
2. Extrae la decisión (tomada o pendiente, y de quién), el compromiso, el puesto responsable, la fecha y el resultado reportado.
3. Busca coincidencias semánticas con los hilos abiertos para no duplicar.
4. Deja su propuesta en el borrador (§4.2) con la cita que la justifica.
5. Aprende de las ediciones y descartes del usuario: glosario de apodos, siglas, códigos de producto y criterios de qué sí es un hilo.

### 4.2 Borrador de tareas a agregar **[D]**

Bandeja con dos secciones:

- **Nuevos temas detectados.** Por cada uno, el usuario:
  - lo **convierte en hilo**, editando antes o después el detalle, la fecha esperada, el puesto responsable (cualquier puesto de la organización), el área, el proyecto y las subtareas; o
  - lo **descarta**, con una razón opcional que el motor usa para aprender.
- **Actualizaciones sugeridas** a hilos existentes (por ejemplo, "ya se entregó" pasa a `En revisión`): se aceptan o se rechazan con un toque.

Un hilo es editable en todo momento y cada cambio queda en la bitácora. En la Fase 2, cada usuario tiene su propio borrador con lo detectado en sus conversaciones.

### 4.3 Acta del 1:1 por correo **[D]**

- Al terminar el 1:1, quien lo dirige envía un correo sencillo al otro participante con **copia a `hilos@hrsuplidora.com`**. El cuerpo es libre: una lista de temas, y si se quiere, responsable y fecha. No hace falta plantilla.
- HILOS lo procesa en menos de 5 minutos **[S]**:
  - lo que se refiere a un hilo existente se actualiza;
  - lo nuevo se crea como hilo, porque quien envía el acta ya lo validó;
  - lo ambiguo (sin responsable claro, por ejemplo) queda en el borrador.
- HILOS responde al remitente con una confirmación: qué cargó, qué actualizó, qué quedó en borrador y el enlace.
- Ambos participantes quedan con el mismo registro por escrito. Eso elimina las versiones distintas de un mismo acuerdo.
- Solo se aceptan actas de cuentas internas verificadas (§6).

### 4.4 Captura manual

Todo dentro de la aplicación HILOS (§7), más dos atajos:

- Botón "+ Hilo" en la aplicación web, que también se instala en el celular como ícono (PWA, sin tienda de aplicaciones).
- Reenviar un correo (también de externos) a `hilos@hrsuplidora.com` con una nota: queda en el borrador.
- En Slack: comando `/hilo` o reacción 🧵 sobre un mensaje, que también queda en el borrador.

### 4.5 Publicación del lunes 6:45 a.m. **[D]**

- Una publicación por cada puesto que reporta a la Gerencia General, más una vista consolidada. Se envía por correo a las 6:45 a.m. hora de Costa Rica y queda en la aplicación.
- Secciones:
  1. Requiere decisión de la Gerencia General, con días de espera.
  2. Requiere decisión del puesto.
  3. Novedades de la semana, con evidencia.
  4. En ejecución, con nivel de implementación, fecha, avance de subtareas y semáforo.
  5. Alertas: vencidos, más de 14 días sin movimiento, sin fecha o sin responsable, acuerdos contradictorios.
  6. Resultados por medir.
  7. Pendientes en el borrador.
  8. Cerrados en la semana.
  9. Preguntas sugeridas.
- En la Fase 2, cada puesto recibe también su propia publicación, para que ambos lleguen al 1:1 con la misma lista.

### 4.6 Vistas

- Por puesto: la publicación viva.
- Lo que espera de la Gerencia General.
- Por área.
- Por proyecto.
- Tablero por nivel de implementación.
- Línea de tiempo.
- OKR.
- Archivo.
- Desempeño (§4.9).

### 4.7 Termómetro de delegación

Indicadores semanales:

- Decisiones pendientes de la Gerencia General: cantidad y días promedio de espera.
- Porcentaje de hilos cerrados sin intervención de la Gerencia.
- Porcentaje de hilos con un puesto responsable distinto de la Gerencia General.

### 4.8 Notificaciones

- Publicación del lunes.
- Recordatorio semanal a cada responsable con lo que vence.
- Confirmación de actas.
- Aviso de borrador acumulado.

En la Fase 1, HILOS absorbe el resumen diario que hoy corre en Zapier.

### 4.9 Evaluación de cumplimiento y desempeño **[D]**

Se usa la misma escala que hoy se aplica en Asana:

| Dimensión | Opciones |
|---|---|
| **Entrega** | A tiempo · Tarde – Justificado · Tarde – Injustificado |
| **Ejecución** | Mejor de lo esperado · Lo esperado · Menos de lo esperado |

- Se evalúa al marcar un hilo o subtarea como `Completada`. Quien revisa (quien asignó o el superior del puesto) escoge ambas dimensiones.
- HILOS sugiere la entrega comparando la fecha comprometida con la de cierre. La justificación de un atraso la decide quien revisa.
- La evaluación queda a nombre de la persona que ejecutó; el hilo, a nombre del puesto.
- La vista de Desempeño muestra por persona y período:
  - cuántos hilos tiene evaluados;
  - la distribución de entrega y de ejecución;
  - el porcentaje a tiempo.
- Las reprogramaciones de fecha quedan registradas en el historial de cada hilo.
- Si estos datos se usan para decisiones de compensación o disciplinarias, los criterios deben comunicarse de antemano y coordinarse con RRHH. Conviene validar con un abogado laboralista.

### 4.10 Permisos y confidencialidad

- La Gerencia General ve todo.
- Cada puesto ve sus hilos, los de sus reportes y los que comparte con pares.
- Los hilos marcados como confidenciales (salarios, disciplinarios, salud) los ven solo las personas autorizadas.
- Los permisos se aplican en la base de datos, no solo en pantalla.

## 4bis. Fase 2: un solo registro, vistas por rol y cero duplicados

### Un hilo, no una copia por persona

Todos los hilos viven en una sola base. Cada hilo tiene:

- **Puesto responsable:** quien ejecuta.
- **Solicitante:** quien lo pidió.
- **Espera decisión de:** si está frenado, quién debe decidir.
- **Seguidores** (opcional).

No existe una "tarea de dar seguimiento" separada: dar seguimiento es ser el solicitante del hilo.

| Quién | Qué ve |
|---|---|
| Gerencia General | Todo. Su Publicación por puesto, como hoy. |
| Reporte directo | **Mis hilos:** donde su puesto es responsable. **Lo que pedí:** donde es solicitante. **Mi equipo:** los hilos de sus subordinados. **Espera mi decisión.** |
| Colaborador sin reportes | Sus hilos y lo que pidió. |

Si usted cambia la fecha del hilo #045, su reporte ve el cambio en su panel al instante, y viceversa. Queda registrado quién cambió qué.

### Quién ve qué (visibilidad) **[D] Opción B**

Las reglas se aplican en la base de datos (seguridad por fila), no solo en pantalla.

| Regla | Ve el hilo |
|---|---|
| Participación | El puesto responsable, el solicitante, quien debe decidir y los seguidores. |
| Jerarquía | El superior del puesto responsable y, hacia arriba, toda la cadena hasta la Gerencia General. |
| Entre pares | **No** se ven entre sí **[D]**: cada gerente ve solo lo suyo, lo de su equipo y aquello en que participa. Se descartó la visibilidad de lectura entre gerentes (opción A). |
| Subtareas **[D]** | Quien tiene una subtarea, y su jefe, ve la subtarea completa y un **contexto mínimo** del hilo padre en solo lectura: número, título, puesto responsable, estado y fecha. No ve el detalle del padre, su evidencia ni las otras subtareas. Si el padre es confidencial, solo ve "Hilo confidencial". |
| Colaboradores sin reportes | Solo lo suyo y aquello en que participan. |
| Confidencial | Prevalece sobre todo lo anterior: solo la Gerencia General, el puesto responsable y las personas agregadas explícitamente. |

Editar un hilo solo lo pueden hacer el responsable, el solicitante y la cadena jerárquica hacia arriba. El administrador técnico de respaldo administra cuentas y accesos, pero no tiene por eso visibilidad del contenido de los hilos.

### Cómo se evita la duplicación (cinco barreras)

1. **Identificador único del correo.** El mismo correo tiene el mismo `internetMessageId` en sus Enviados y en la Bandeja del destinatario. HILOS lleva **un registro global** de correos procesados, no uno por buzón: el correo se procesa una vez, desde el primer buzón donde aparece, y en el otro se salta.
2. **Conversación.** Las respuestas del mismo hilo de correo (`conversationId`) se agregan como evidencia o actualización del hilo existente. No crean uno nuevo.
3. **Coincidencia por significado.** Un correo distinto sobre el mismo tema se compara con los hilos abiertos (puesto, área, proyecto y similitud del texto). Por ejemplo, el reporte reenvía la instrucción a su equipo. Si coincide, se propone como actualización o como **subtarea** del hilo existente, no como un hilo nuevo.
4. **Un solo procesamiento, en orden.** Una sola tarea central lee todos los buzones, uno tras otro, contra el mismo registro. Dos lecturas en paralelo no pueden crear el mismo hilo.
5. **Confirmación humana.** El tema detectado va al Borrador de **quien lo pidió**. Si el sistema sospecha un duplicado, lo marca "Posible duplicado de #045", con un botón para fusionar. Al guardarlo, aparece directamente en los hilos del responsable, sin pasar por su borrador.

## 5. Escalabilidad organizacional

Espacios por área, proyectos con plantillas (lanzamiento de producto, importación de China), tareas recurrentes, comentarios con @menciones y adjuntos enlazados a SharePoint. La sustitución de Asana en Mercadeo se decide comparando uso real, flujo creativo y costo. Más adelante, se integra con SAP B1 para medir resultados con datos duros.

## 6. Seguridad

Ningún sistema es inmune. La meta es defensa en capas: que una falla en una capa no exponga la información, que todo quede registrado y que un incidente se detecte y se contenga rápido.

| Capa | Medidas |
|---|---|
| **Identidad** | Solo inicio de sesión con cuentas de Microsoft 365 de HR Suplidora, sin contraseñas propias de HILOS. MFA obligatoria por política de acceso condicional de Entra. Sesiones con expiración. |
| **Autorización** | Permisos por puesto aplicados en la base de datos (seguridad a nivel de fila). Mínimo privilegio en todo. |
| **Acceso a correo** | Aplicación registrada en Entra con permiso de **solo lectura** y limitada a los buzones autorizados (RBAC para aplicaciones de Exchange Online). Autenticación por certificado, no por clave, con rotación programada. El buzón `hilos@` es compartido y no tiene inicio de sesión propio. |
| **IA sin poderes** | El motor de IA no tiene herramientas: no envía correos, no borra ni modifica nada. Solo devuelve una propuesta en formato estructurado que el sistema valida. El contenido de los correos se trata como dato y nunca como instrucción. Así un correo malicioso no puede ordenarle nada al sistema. |
| **Actas entrantes** | Se aceptan solo de remitentes internos, con verificación de autenticidad del correo (SPF, DKIM y DMARC aprobados) y remitente activo en el directorio. Esto evita correos falsificados que inyecten tareas. |
| **Minimización de datos** | Se guardan extractos y enlaces, no copias completas de los correos. Retención definida. Cifrado en tránsito y en reposo. |
| **Secretos** | Llaves y certificados solo en las bóvedas de configuración de Vercel y Supabase. Nunca en el código, en el chat ni en sesiones de desarrollo. Escaneo de secretos en GitHub con bloqueo de envío. |
| **Código** | Rama principal protegida: todo cambio entra por pull request con pruebas aprobadas y aprobación humana. Revisión de seguridad automática en cada cambio. Alertas y actualización de dependencias vulnerables. |
| **Ambientes** | Desarrollo con datos de prueba, separado de producción. Las vistas previas de cada cambio exigen inicio de sesión. |
| **Monitoreo** | Bitácora inmutable de accesos y cambios. Alertas por accesos anómalos, picos de gasto de IA o fallos de ingesta. |
| **Continuidad** | Respaldos diarios con prueba de restauración trimestral. Procedimiento de respuesta a incidentes en `docs/`. |
| **Verificación externa** | Prueba de penetración liviana por un tercero antes de abrir el sistema a toda la organización (Fase 3). |

## 7. Arquitectura y herramientas

| Capa | Herramienta |
|---|---|
| Aplicación (web y celular) | Next.js + TypeScript, instalable como PWA, publicada en Vercel |
| Base de datos, permisos y tareas programadas | Supabase (PostgreSQL, inicio de sesión con Microsoft Entra, seguridad por fila, búsqueda semántica) |
| Correo y directorio | Microsoft Graph con aplicación propia de HR Suplidora |
| Slack | Bot en el workspace de HR Suplidora |
| IA | Claude API: Claude Opus 5.5. Se evalúa con datos un filtro previo con Claude Haiku 5.5. |
| Código | GitHub (organización de HR Suplidora, §8) |

```
Correo interno / Slack interno / Acta (hilos@) / Manual
        │
        ▼
Filtro "solo interno" ──► fuera (registrado)
        │
        ▼
Motor IA ──► Borrador ──► usuario: convierte / edita / descarta
        │                      │
        └──► Acta ─────────────┤ (carga directa, lo ambiguo va al borrador)
                               ▼
                 Hilos, subtareas, evaluaciones (Supabase)
                               │
          ┌────────────────────┼─────────────────────┐
          ▼                    ▼                     ▼
   Aplicación web/celular  Lunes 6:45 a.m.     Termómetro y desempeño
```

## 8. Cuentas, accesos y continuidad

Principio: **todo servicio vive en una cuenta de la empresa, con al menos dos administradores y acceso por rol**, para que cualquiera de ellos pueda operar si la Gerencia General no está. Ninguna cuenta personal es indispensable.

| Servicio | Cómo se organiza | Quién tiene acceso |
|---|---|---|
| **GitHub** | Organización de HR Suplidora (por ejemplo, `github.com/hrsuplidora`). Se transfiere ahí el repositorio actual, que conserva historial e incidencias. Plan Team (~USD 4 por usuario al mes, verificar), necesario para proteger la rama principal en repositorios privados. | Dueños: Gerencia General y un administrador de respaldo. Desarrolladores externos: miembros con acceso solo a este repositorio. Nadie ve los repositorios personales. |
| **Claude (desarrollo)** | La cuenta personal sigue sirviendo para desarrollar. A mediano plazo conviene una cuenta Claude de la empresa (plan Team) con el correo corporativo. | Un tercero que desarrolle usa su propia cuenta de Claude y trabaja sobre el repositorio de la organización. Nunca entra a la cuenta de la Gerencia General. |
| **Claude API (producción)** | Organización de HR Suplidora en la consola de Anthropic, con correo corporativo y tarjeta de la empresa. Espacios separados de desarrollo y producción, con tope de gasto y alertas. | Administradores: Gerencia General y respaldo. Las llaves viven solo en Vercel y Supabase. |
| **Supabase y Vercel** | Organización o equipo a nombre de HR Suplidora, con correo corporativo. | Dueños: Gerencia General y respaldo. Desarrollador: acceso a desarrollo; a producción solo si se autoriza. |
| **Microsoft 365** | Aplicación HILOS registrada en el Entra de la empresa. Buzón compartido `hilos@` (no requiere licencia). | Administradores globales de Microsoft 365 (Gerencia General y respaldo). |
| **Credenciales** | Gestor de contraseñas empresarial con bóveda "HILOS – infraestructura" y acceso de emergencia. MFA en todas las cuentas. | Gerencia General y respaldo. |
| **Documentación** | `docs/operacion.md`: quién tiene acceso a qué, cómo se rotan llaves, cómo se restaura y cómo se da o quita acceso. | Repositorio. |

**[D]** Responsables:

| Rol | Puesto | Cuenta |
|---|---|---|
| Administrador principal | Gerencia General | jmunoz@hrsuplidora.com |
| Administrador de respaldo | Gerencia de Operaciones | jquesada@hrsuplidora.com |
| Gestión de pagos y facturación | Asistente Contable | gestion@hrsuplidora.com |
| Administración de Microsoft 365 (Entra, buzón `hilos@`, registro de la aplicación) | Gerencia General | jmunoz@hrsuplidora.com |

La Asistente Contable entra solo a la parte de facturación de cada servicio (Anthropic, Supabase, Vercel, GitHub), sin acceso a datos ni a código.

## 9. Costos

### 9.1 Qué cuesta y qué no

- **Revisar cada 15 minutos si hay correos o mensajes nuevos no tiene costo relevante.** Microsoft Graph y la API de Slack no cobran por consulta: está incluido en las licencias actuales, dentro de sus límites de uso. La tarea programada corre dentro del plan de Supabase.
- **Lo que cuesta es procesar cada mensaje con IA**, y cada mensaje se procesa una sola vez, cualquiera que sea la frecuencia. Revisar cada 15 minutos o una vez al día cuesta prácticamente lo mismo.
- **Lo que sí ahorra es agrupar.** Procesar en lote dos veces al día con la Batch API cuesta 50% menos que procesar al instante, y procesar la conversación completa da mejor contexto y menos duplicados. Las actas se procesan al instante.

### 9.2 Volumen medido **[H]**

Buzón de la Gerencia General, del 28 de septiembre al 11 de octubre de 2026 (2 semanas):

| Concepto | Correos |
|---|---|
| Recibidos de remitentes internos | 116 (37 la primera semana, 79 la segunda) |
| De esos, automáticos de sistemas (gestión documental, notificaciones) | ~23 |
| De esos, invitaciones o respuestas de calendario | ~8 |
| **Recibidos internos escritos por personas** | **~85** |
| Enviados con solo destinatarios internos | 74 (~67 sin contar aceptaciones de reunión ni pruebas) |
| Enviados con destinatarios internos y externos (quedan fuera por la regla de §3.1) | 12 |
| Asuntos distintos entre los recibidos internos | ~75–79 (~66 sin los de sistemas) |

Proyección **[S]**: entre 250 y 400 mensajes internos al mes en las conversaciones de la Gerencia General, agrupados en unas 140 conversaciones. Dos semanas son una muestra corta y el volumen varió el doble de una semana a otra.

### 9.3 Estimación mensual **[S]**

Tipo de cambio de referencia: ₡507 por USD. Precios de la Claude API vigentes a octubre de 2026. Los de Supabase, Vercel y GitHub son referencias públicas por verificar.

| Rubro | USD/mes | CRC/mes |
|---|---|---|
| Claude API, Fase 1: ~300–350 mensajes, publicación del lunes y actas | 15–35 | ₡7.600–17.700 |
| Supabase (Pro) | ~25 | ~₡12.700 |
| Vercel (Pro, 1 usuario) | ~20 | ~₡10.100 |
| GitHub (Team, 2 usuarios) | ~8 | ~₡4.100 |
| **Total Fase 1** | **~70–90** | **~₡34.500–44.600** |
| **Total Fase 2** (5 buzones más Slack; IA de 50 a 150) | **~105–205** | **~₡53.000–104.000** |

Notas:

- **Costo por mensaje:** cerca de USD 0,06 (₡30) procesado al instante y USD 0,03 (₡15) en lote, con Claude Opus 5.5.
- **Frecuencia:** revisar cada 15 minutos o una vez al día no cambia el costo de IA. Procesar en lote ahorra unos USD 10 al mes (~₡5.000) en la Fase 1.
- **Fase 0:** corre dentro de la suscripción actual de Claude de la Gerencia General, sin cobro adicional de API.

## 10. Fases

| Fase | Duración **[S]** | Alcance |
|---|---|---|
| **0. Prototipo** | 3–4 semanas | Corre con la cuenta de Claude de la Gerencia General y el conector actual de Microsoft 365 (solo lectura). Detalle abajo. |
| **1. Aplicación para la Gerencia** | 6–8 semanas | Aplicación completa: ingesta interna, borrador, actas por `hilos@`, áreas, proyectos, subtareas, evaluación, publicación del lunes, seguridad de §6 y cuentas de §8. Absorbe el resumen diario de Zapier. Antes de empezar: depurar los perfiles de Entra. |
| **2. Puestos que reportan a la Gerencia** | 6–8 semanas | Acceso de los reportes, borrador propio, Slack, sus buzones, publicación propia, política de uso comunicada al personal. |
| **3. Organización** | Por definir | Espacios por área, plantillas, prueba de penetración, decisión sobre Asana, SAP B1. |

Detalle de la Fase 0:

- **Página:** https://claude.ai/artifact/WieamYskCoDZPrfRq2D3Ww. Es privada y solo la Gerencia General puede leer sus datos.
- **Lectura del correo:** de lunes a viernes a las 6:50 p. m., y el lunes a las 5:50 a. m. antes de la publicación.
- **Publicación del lunes:** lista antes de las 6:45 a. m., con aviso al celular a las 6:45.
- **Actas:** un correo interno con asunto que empiece con "Acta". Se cargan en la lectura de ese mismo día.
- **Borrador:** se gestiona desde la página. Se puede convertir, editar o descartar.
- **Captura manual:**
  - el botón "+ Hilo" de la página;
  - un correo a uno mismo con asunto que empiece con "HILO:", lo que también sirve para reenviarse un correo externo.

Criterios para pasar a la Fase 1:

- Al menos 80% de lo detectado es útil.
- El borrador toma menos de 15 minutos por semana.
- Los campos, los estados y la evaluación quedan validados.

## 11. Gestión del proyecto con Claude en la nube

**Papeles separados:**

- La Gerencia General es la dueña de producto: decide y aprueba.
- Claude Code en la nube es el equipo de desarrollo.
- La Claude API dentro de HILOS es el motor de producción. Corre con cuentas de la empresa y no depende de sesiones de Claude Code ni de cuentas personales.

**Repositorio como memoria:**

- `CLAUDE.md` con el contexto del negocio y las reglas.
- `docs/` con esta propuesta, las decisiones tomadas y la operación.
- El backlog en GitHub Issues, por fase.

Cualquier desarrollador con acceso al repositorio puede continuar el trabajo.

**Ciclo de cada cambio:**

1. Solicitud en español.
2. Claude crea una rama, implementa, prueba y abre un pull request con revisión de seguridad.
3. La Gerencia revisa la vista previa en el celular y aprueba.
4. El cambio se publica automáticamente.

**Entorno de desarrollo:**

- Las llaves de desarrollo se guardan en la configuración del entorno de la nube, nunca en el chat.
- Solo se habilitan los dominios necesarios.
- Un script de inicio instala dependencias y corre pruebas.
- Las credenciales de producción nunca entran a una sesión de desarrollo.

**Calidad de la IA:** las ediciones y descartes del borrador en la Fase 0 forman el set de prueba. Ningún cambio al motor se publica sin superarlo.

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Perfiles de Entra desordenados: el sistema asigna mal los puestos. | Depuración previa a la Fase 1 y sincronización diaria con alertas de inconsistencias (puesto sin jefe, cargo fuera del catálogo). |
| Temas importantes que solo existen con externos. | Captura manual y reenvío a `hilos@`. Revisar en la Fase 0 cuánto se pierde. |
| Errores de la IA. | Borrador con decisión humana, evidencia obligatoria y set de prueba. |
| Baja adopción, como con Planner. | Fase 2 solo después de cuatro semanas de uso por la Gerencia General. Las actas dan valor inmediato a los reportes. |
| Evaluación de desempeño percibida como vigilancia. | Criterios conocidos de antemano, coordinados con RRHH y aplicados igual a todos los puestos. |
| Dependencia de la Gerencia General. | Cuentas de empresa con respaldo (§8) y dueño funcional interno desde la Fase 2. |
| Costo de IA. | Tope mensual con alertas, procesamiento en lote y caché. |

## 13. Estado y pendientes

**[D]** La Fase 0 arrancó el 12 de octubre de 2026. El detalle operativo está en `fase0/RUTINA.md`.

Pendientes para la Fase 1:

1. ~~Crear la organización de GitHub de HR Suplidora y transferir el repositorio.~~ **Hecho el 12 de octubre de 2026:** `github.com/hrsuplidora/Hilos`, con la app de Claude instalada.
2. Depurar los perfiles de Entra ID: cargo, departamento y jefe directo de cada cuenta, incluidas las de rol (Gerencia General).
3. Crear el buzón compartido `hilos@hrsuplidora.com` (Gerencia General).
4. Crear las cuentas de Anthropic (API), Supabase y Vercel a nombre de HR Suplidora con los responsables de §8 (Gerencia General y Asistente Contable).
