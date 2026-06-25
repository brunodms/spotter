from django.test import TestCase
from core.forms.auth import RegistroForm
from core.models import Usuario, PerfilAluno, PerfilPersonal

class RegistroFormTest(TestCase):
    def test_registro_aluno_valido(self):
        data = {
            'nome': 'João Aluno',
            'email': 'joao@teste.com',
            'tipo': Usuario.ALUNO,
            'password1': 'senha_segura_123',
            'password2': 'senha_segura_123',
        }
        form = RegistroForm(data=data)
        self.assertTrue(form.is_valid())
        
        # Salva o form e verifica a criação do PerfilAluno
        user = form.save()
        self.assertEqual(user.tipo, Usuario.ALUNO)
        self.assertTrue(PerfilAluno.objects.filter(usuario=user).exists())

    def test_registro_personal_valido(self):
        data = {
            'nome': 'Maria Personal',
            'email': 'maria@teste.com',
            'tipo': Usuario.PERSONAL,
            'cref': '123456-G/SP',
            'password1': 'senha_segura_123',
            'password2': 'senha_segura_123',
        }
        form = RegistroForm(data=data)
        self.assertTrue(form.is_valid())
        
        # Salva o form e verifica a criação do PerfilPersonal
        user = form.save()
        self.assertEqual(user.tipo, Usuario.PERSONAL)
        self.assertTrue(PerfilPersonal.objects.filter(usuario=user, cref='123456-G/SP').exists())

    def test_registro_personal_sem_cref_invalido(self):
        data = {
            'nome': 'Maria Personal',
            'email': 'maria2@teste.com',
            'tipo': Usuario.PERSONAL,
            'cref': '',  # CREF vazio
            'password1': 'senha_segura_123',
            'password2': 'senha_segura_123',
        }
        form = RegistroForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('cref', form.errors)

    def test_registro_senhas_nao_coincidem(self):
        data = {
            'nome': 'Carlos',
            'email': 'carlos@teste.com',
            'tipo': Usuario.ALUNO,
            'password1': 'senha123',
            'password2': 'senha456',  # Senhas diferentes
        }
        form = RegistroForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_registro_email_duplicado(self):
        # Cria um usuário primeiro
        Usuario.objects.create_user(email='duplicado@teste.com', nome='Teste', password='123')
        
        data = {
            'nome': 'Novo Teste',
            'email': 'duplicado@teste.com',
            'tipo': Usuario.ALUNO,
            'password1': 'senha_segura_123',
            'password2': 'senha_segura_123',
        }
        form = RegistroForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
