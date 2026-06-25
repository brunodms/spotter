from django.test import TestCase
from core.models import Usuario, PerfilAluno, PerfilPersonal, Contrato, PlanoTreino, SessaoTreino, Exercicio

class TreinosTest(TestCase):
    def setUp(self):
        user_aluno = Usuario.objects.create_user('aluno@teste.com', 'Aluno', '123', tipo=Usuario.ALUNO)
        user_personal = Usuario.objects.create_user('personal@teste.com', 'Personal', '123', tipo=Usuario.PERSONAL)
        
        self.aluno = PerfilAluno.objects.create(usuario=user_aluno)
        self.personal = PerfilPersonal.objects.create(usuario=user_personal, cref='1234')
        self.contrato = Contrato.objects.create(aluno=self.aluno, personal=self.personal)
        self.contrato.aceitar()

    def test_criacao_e_codigo_sequencial_plano_treino(self):
        plano1 = PlanoTreino.objects.create(contrato=self.contrato, nome='Hipertrofia A')
        self.assertEqual(plano1.codigo, 1)
        self.assertEqual(plano1.ativo, True)
        
        plano2 = PlanoTreino.objects.create(contrato=self.contrato, nome='Hipertrofia B')
        self.assertEqual(plano2.codigo, 2)

    def test_criacao_e_codigo_sequencial_sessao_treino(self):
        plano = PlanoTreino.objects.create(contrato=self.contrato, nome='Plano')
        
        sessao1 = SessaoTreino.objects.create(plano=plano, nome='Treino de Peito')
        self.assertEqual(sessao1.codigo, 1)
        self.assertEqual(sessao1.ordem, 1)
        
        sessao2 = SessaoTreino.objects.create(plano=plano, nome='Treino de Costas')
        self.assertEqual(sessao2.codigo, 2)
        
    def test_criacao_e_codigo_sequencial_exercicio(self):
        plano = PlanoTreino.objects.create(contrato=self.contrato, nome='Plano')
        sessao = SessaoTreino.objects.create(plano=plano, nome='Sessao')
        
        ex1 = Exercicio.objects.create(
            sessao=sessao,
            nome='Supino Reto',
            series=4,
            repeticoes=12
        )
        self.assertEqual(ex1.codigo, 1)
        
        ex2 = Exercicio.objects.create(
            sessao=sessao,
            nome='Supino Inclinado',
            series=3,
            repeticoes=10
        )
        self.assertEqual(ex2.codigo, 2)

    def test_delecao_em_cascata(self):
        # Garante que se o plano for deletado, sessões e exercícios também somem
        plano = PlanoTreino.objects.create(contrato=self.contrato, nome='Plano Deletar')
        sessao = SessaoTreino.objects.create(plano=plano, nome='Sessao')
        Exercicio.objects.create(sessao=sessao, nome='Ex1', series=3, repeticoes=10)
        
        self.assertEqual(Exercicio.objects.count(), 1)
        self.assertEqual(SessaoTreino.objects.count(), 1)
        
        plano.delete()
        
        self.assertEqual(SessaoTreino.objects.count(), 0)
        self.assertEqual(Exercicio.objects.count(), 0)
