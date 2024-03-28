from rest_framework import serializers
from cadastro.models import Curso

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ('id','nome','duracao','valor','vagas_totais', 'faturamento')


