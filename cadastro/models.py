from django.db import models
    
class Curso(models.Model):
    nome = models.CharField(max_length=50)
    duracao = models.IntegerField()
    valor = models.FloatField()
    vagas_totais = models.IntegerField()
    faturamento = models.FloatField(default=0)
    
    def __str__(self):
        return self.nome

