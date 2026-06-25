from django.test import TestCase
from core.models import Usuario, PerfilAluno, PerfilPersonal, Contrato, Avaliacao

class AvaliacaoTest(TestCase):
    def setUp(self):
        # Setup: Criamos alunos e personais
        user_aluno = Usuario.objects.create_user('aluno@teste.com', 'Aluno', '123', tipo=Usuario.ALUNO)
        user_personal = Usuario.objects.create_user('personal@teste.com', 'Personal', '123', tipo=Usuario.PERSONAL)
        
        self.aluno = PerfilAluno.objects.create(usuario=user_aluno)
        self.personal = PerfilPersonal.objects.create(usuario=user_personal, cref='1234')
        
        self.contrato = Contrato.objects.create(aluno=self.aluno, personal=self.personal)

    def test_nao_pode_avaliar_contrato_pendente(self):
        # O contrato criado no setUp está PENDENTE
        avaliacao = Avaliacao(
            contrato=self.contrato,
            aluno=self.aluno,
            personal=self.personal,
            nota=5,
            comentario='Excelente!'
        )
        
        with self.assertRaises(ValueError):
            avaliacao.save()

    def test_pode_avaliar_contrato_ativo(self):
        self.contrato.aceitar()
        
        avaliacao = Avaliacao.objects.create(
            contrato=self.contrato,
            aluno=self.aluno,
            personal=self.personal,
            nota=5,
            comentario='Excelente!'
        )
        
        self.assertEqual(Avaliacao.objects.count(), 1)
        self.assertEqual(avaliacao.nota, 5)

    def test_atualiza_media_do_personal(self):
        self.contrato.aceitar()
        
        Avaliacao.objects.create(
            contrato=self.contrato,
            aluno=self.aluno,
            personal=self.personal,
            nota=4,
            comentario='Muito bom!'
        )
        
        # A média é atualizada pelo método save() da Avaliacao
        self.personal.refresh_from_db()
        self.assertEqual(self.personal.avaliacao_media, 4.0)
        
        # Vamos criar um segundo aluno e contrato para avaliar e mudar a média
        user_aluno2 = Usuario.objects.create_user('aluno2@teste.com', 'Aluno 2', '123', tipo=Usuario.ALUNO)
        aluno2 = PerfilAluno.objects.create(usuario=user_aluno2)
        contrato2 = Contrato.objects.create(aluno=aluno2, personal=self.personal)
        contrato2.aceitar()
        
        Avaliacao.objects.create(
            contrato=contrato2,
            aluno=aluno2,
            personal=self.personal,
            nota=2,
            comentario='Mais ou menos'
        )
        
        self.personal.refresh_from_db()
        # Média deve ser (4 + 2) / 2 = 3.0
        self.assertEqual(self.personal.avaliacao_media, 3.0)
