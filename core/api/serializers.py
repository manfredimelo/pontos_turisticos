from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from atracoes.models import Atracao
from avaliacoes.api.serializers import AvaliacaoSerializer
from comentarios.api.serializers import ComentarioSerializer
from core.models import PontoTuristico
from atracoes.api.serializers import AtracaoSerializer
from enderecos.api.serializers import EnderecoSerializer


class PontoTuristicoSerializer(ModelSerializer):
    atracoes = AtracaoSerializer(many=True)
    endereco = EnderecoSerializer(read_only=True)
    comentarios =ComentarioSerializer(many=True, read_only=True)
    avaliacoes = AvaliacaoSerializer(many=True, read_only=True)
    descricao_completa = SerializerMethodField()
    class Meta:
        model = PontoTuristico
        fields = ('id', 'nome', 'descricao', 'aprovado', 'foto',
                  'atracoes', 'comentarios', 'avaliacoes', 'endereco',
                  'descricao_completa', 'teste')
        ready_only_fields = {'comentarios', 'avaliacoes'}
    def cia_atracoes(self, atracoes, ponto):
        for atracao in atracoes:
            at =Atracao.objects.create(**atracao)
            ponto.atracoes.add(at)
        return

    def create(self, validated_data):
        atracoes = validated_data['atracoes']
        del validated_data['atracoes']
        ponto = PontoTuristico.opbjects.create(**validated_data)
        self.cia_atracoes(atracoes, ponto)
        return ponto
    def get_descricao_completa(self, obj):

        return '%s - %s ' % (obj.nome, obj.descricao)