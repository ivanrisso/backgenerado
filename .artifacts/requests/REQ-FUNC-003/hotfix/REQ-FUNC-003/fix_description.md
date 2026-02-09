##REQ-FUNC-003

Origen:
Detectado manualmente por el equipo (fuera del Workflow 70).

Síntoma observable:
Los cambios realizados mediante el CRUD de Menúes
(no agregan / eliminan / reordenan items)
NO se reflejan en el menú lateral de la aplicación.

El sidebar mantiene una estructura estática
independiente del estado persistido del CRUD.

Impacto funcional:
El usuario puede configurar menús,
pero no observa ningún efecto en la navegación real,
lo que genera confusión y pérdida de confianza en el sistema.
