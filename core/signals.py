"""Signals para lógica automática do spotter."""

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender="core.Contrato")
def desativar_contratos_anteriores(sender, instance, **kwargs):
    """Garante apenas um contrato ativo por par (personal, aluno)."""
    if instance.status == sender.STATUS_ATIVO:
        sender.objects.filter(
            personal=instance.personal,
            aluno=instance.aluno,
            status=sender.STATUS_ATIVO,
        ).exclude(pk=instance.pk).update(status=sender.STATUS_ENCERRADO)


@receiver(pre_save, sender="core.Avaliacao")
def popular_avaliacao_perfis(sender, instance, **kwargs):
    """Preenche aluno e personal a partir do contrato se não definidos."""
    if not instance.aluno_id:
        instance.aluno = instance.contrato.aluno
    if not instance.personal_id:
        instance.personal = instance.contrato.personal
