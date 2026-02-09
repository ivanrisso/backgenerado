hotfix_id: HF-FUNC-XXX
origen: deteccion_manual
origen_workflow: none
tipo: FUNCIONAL
subtipo: MENU / NAVEGACION

estado: PENDIENTE_DE_CORRECCION

area_afectada:
  - ui
  - navegacion
  - sidebar

sintoma_principal:
  - items_hijos_renderizados_como_principales

impacto_usuario: ALTO

riesgo_funcional:
  - confusion_navegacion
  - exposicion_incorrecta_funcionalidades

requiere_workflow:
  - 72

precondiciones:
  - estructura_de_menu_definida_en_crud
  - correccion_funcional_previa_aplicada

exclusiones:
  - no_correccion_tecnica
  - no_refactor
  - no_nuevas_features

decision_humana_requerida: true
