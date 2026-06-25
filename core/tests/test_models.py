from django.test import TestCase
from core.models import Usuario

class UsuarioModelTest(TestCase):
    def setUp(self):
        # O método setUp roda ANTES de cada teste
        # Ideal para criar dados que serão usados em vários testes
        self.aluno = Usuario.objects.create_user(
            email='aluno@teste.com',
            nome='João Aluno',
            password='1234',
            tipo=Usuario.ALUNO
        )
        
        self.personal = Usuario.objects.create_user(
            email='personal@teste.com',
            nome='Maria Personal',
            password='1234',
            tipo=Usuario.PERSONAL
        )

    def test_criacao_usuario(self):
        # Verifica se o usuário foi salvo no banco e tem os dados corretos
        self.assertEqual(self.aluno.email, 'aluno@teste.com')
        self.assertEqual(self.aluno.nome, 'João Aluno')
        # Verifica se a senha foi hasheada (não é igual ao texto puro)
        self.assertNotEqual(self.aluno.password, '1234')
        self.assertTrue(self.aluno.check_password('1234'))

    def test_properties_tipo_usuario(self):
        # Verifica as propriedades eh_aluno e eh_personal
        self.assertTrue(self.aluno.eh_aluno)
        self.assertFalse(self.aluno.eh_personal)
        
        self.assertTrue(self.personal.eh_personal)
        self.assertFalse(self.personal.eh_aluno)

    def test_str_representation(self):
        # Verifica se o método __str__ retorna o texto esperado
        self.assertEqual(str(self.aluno), 'João Aluno (Aluno)')
        self.assertEqual(str(self.personal), 'Maria Personal (Personal Trainer)')
