from rest_framework import serializers
from .models import Periodo, Funcionario


class SerializerPeriodo(serializers.ModelSerializer):

    class Meta:
        model = Periodo


class SerializerFuncionario(serializers.ModelSerializer):
    periodos = serializers.RelatedField(many=True)

    class Meta:
        model = Funcionario