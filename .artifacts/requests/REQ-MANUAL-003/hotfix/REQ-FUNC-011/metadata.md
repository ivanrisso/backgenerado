hotfix_id: HF-FUNC-MENU-FE-ORDER-COLLAPSE
tipo: FUNCIONAL
workflow_ejecucion: 72

origen:
  tipo: requerimiento_funcional
  detectado_en: frontend
  contexto: configuracion_de_menues
  detectado_por: humano

area_afectada: frontend
modulo: menus
submodulo: configuracion_menus_y_sidebar

problema_principal:
  descripcion: >
    El frontend no permite definir ni reflejar correctamente
    la jerarquía y el orden de los ítems de menú, generando
    inconsistencias entre la configuración administrativa
    y la navegación real del usuario.

capacidades_afectadas:
  - colapso_menus_padre
  - jerarquia_padre_hijo
  - orden_menus_padre
  - orden_menus_hijo
  - render_sidebar

comportamiento_actual:
  - menus_padre_no_colapsables
  - orden_por_insercion
  - hijos_renderizados_como_principales
  - orden_no_gobernado_por_configuracion

comportamiento_esperado:
  - menus_padre_colapsables_en_crud
  - hijos_renderizados_solo_bajo_su_padre
  - orden_configurable_para_padres
  - orden_configurable_para_hijos
  - orden_provisto_por_api_backend
  - sidebar_respeta_orden_y_jerarquia

impacto:
  usuario: alto
  funcional: navegacion_inconsistente
  severidad: media

alcance:
  incluye:
    - frontend_crud_menus
    - frontend_sidebar
  excluye:
    - reglas_de_negocio
    - cambios_no_relacionados

requiere_backend:
  orden_provisto_por_api: true
  cambios_backend_requeridos: false

estado: LISTO_PARA_EJECUCION
