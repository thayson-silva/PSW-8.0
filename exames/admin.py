from django.contrib import admin
from .models import PedidosExames, SolicitacaoExame, TiposExames

@admin.register(TiposExames)
class TiposExamesAdmin(admin.ModelAdmin):
    ...
# admin.site.register(TiposExames)

admin.site.register(PedidosExames)
admin.site.register(SolicitacaoExame)