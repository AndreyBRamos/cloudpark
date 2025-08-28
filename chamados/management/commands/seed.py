from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chamados.models import Ticket, Profile

class Command(BaseCommand):
    help = "Cria usuários demo e alguns tickets de exemplo."

    def handle(self, *args, **options):
        def ensure_profile(user, role):
            # garante que sempre haverá Profile, mesmo para usuários antigos
            profile, _ = Profile.objects.get_or_create(user=user, defaults={"role": role})
            # se já existia profile, atualiza o role conforme desejado
            if profile.role != role:
                profile.role = role
                profile.save()
            return profile

        def mkuser(username, password, role):
            user, created = User.objects.get_or_create(
                username=username, defaults={"email": username}
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Usuário criado: {username} ({role})"))
            else:
                self.stdout.write(self.style.WARNING(f"Usuário já existe: {username}"))

            ensure_profile(user, role)  # <- linha-chave
            return user

        atendente = mkuser("atendente@demo.com", "123456", "ATENDENTE")
        tecnico   = mkuser("tecnico@demo.com",   "123456", "TECNICO")

        if not Ticket.objects.exists():
            Ticket.objects.create(
                titulo="Computador não liga",
                descricao="Ao apertar o power, nada acontece.",
                prioridade="ALTA",
                setor="TI",
                status="ABERTO",
                criado_por=atendente,
                atribuido_a=tecnico,
            )
            Ticket.objects.create(
                titulo="Impressora sem papel",
                descricao="Solicitar reposição de papel.",
                prioridade="BAIXA",
                setor="Admin",
                status="EM_ATENDIMENTO",
                criado_por=atendente,
                atribuido_a=tecnico,
            )
            self.stdout.write(self.style.SUCCESS("Tickets de exemplo criados."))
        else:
            self.stdout.write(self.style.WARNING("Já existem tickets no banco."))
