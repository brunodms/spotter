from django.test import TestCase
from core.models import Usuario, PerfilAluno, PerfilPersonal, Contrato

class ContratoTest(TestCase):
    def setUp(self):
        # Setup: Criamos 1 aluno e 1 personal
        user_aluno = Usuario.objects.create_user('aluno@teste.com', 'Aluno', '123', tipo=Usuario.ALUNO)
        user_personal = Usuario.objects.create_user('personal@teste.com', 'Personal', '123', tipo=Usuario.PERSONAL)
        
        # Como o form não está rodando aqui, criamos os perfis manualmente
        self.aluno = PerfilAluno.objects.create(usuario=user_aluno)
        self.personal = PerfilPersonal.objects.create(usuario=user_personal, cref='1234')

    def test_contrato_criado_como_pendente(self):
        contrato = Contrato.objects.create(aluno=self.aluno, personal=self.personal)
        self.assertEqual(contrato.status, Contrato.STATUS_PENDENTE)
        self.assertIsNone(contrato.aceito_em)
        self.assertIsNone(contrato.encerrado_em)

    def test_aceitar_contrato(self):
        contrato = Contrato.objects.create(aluno=self.aluno, personal=self.personal)
        contrato.aceitar()
        
        self.assertEqual(contrato.status, Contrato.STATUS_ATIVO)
        self.assertIsNotNone(contrato.aceito_em)
        self.assertTrue(contrato.esta_ativo)

    def test_aceitar_contrato_encerra_anteriores_ativos(self):
        # Contrato antigo que estava ativo
        contrato_antigo = Contrato.objects.create(aluno=self.aluno, personal=self.personal)
        contrato_antigo.aceitar()
        
        # Novo contrato entra
        contrato_novo = Contrato.objects.create(aluno=self.aluno, personal=self.personal)
        contrato_novo.aceitar()
        
        # Verifica se o antigo foi encerrado
        contrato_antigo.refresh_from_db()
        self.assertEqual(contrato_antigo.status, Contrato.STATUS_ENCERRADO)
        self.assertIsNotNone(contrato_antigo.encerrado_em)
        
        # Verifica se o novo está ativo
        self.assertEqual(contrato_novo.status, Contrato.STATUS_ATIVO)

    def test_recusar_contrato(self):
        contrato = Contrato.objects.create(aluno=self.aluno, personal=self.personal)
        contrato.recusar()
        
        self.assertEqual(contrato.status, Contrato.STATUS_RECUSADO)
        self.assertIsNotNone(contrato.encerrado_em)

    def test_encerrar_contrato(self):
        contrato = Contrato.objects.create(aluno=self.aluno, personal=self.personal)
        contrato.aceitar()
        
        contrato.encerrar()
        self.assertEqual(contrato.status, Contrato.STATUS_ENCERRADO)
        self.assertIsNotNone(contrato.encerrado_em)

    def test_nao_pode_aceitar_contrato_nao_pendente(self):
        contrato = Contrato.objects.create(aluno=self.aluno, personal=self.personal)
        contrato.aceitar()  # Agora está ativo
        
        # Tentar aceitar de novo deve gerar ValueError
        with self.assertRaises(ValueError):
            contrato.aceitar()

    def test_nao_pode_recusar_contrato_nao_pendente(self):
        contrato = Contrato.objects.create(aluno=self.aluno, personal=self.personal)
        contrato.aceitar()  # Agora está ativo
        
        # Tentar recusar algo que já está ativo deve gerar ValueError
        with self.assertRaises(ValueError):
            contrato.recusar()
