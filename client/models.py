from django.db import models
from employee.models import Employee
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4

class Client (models.Model) : 
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    picture = models.ImageField(upload_to='clients-images/',default='default.png')
    problem = models.TextField()

    def __str__(self) : 
        return self.full_name
    
class Ticket (models.Model) : 
    id = models.UUIDField(default=uuid4,editable=False,db_index=True,primary_key=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)

    def __str__(self) : 
        return self.client.problem
    


@receiver(post_save, sender=Client)
def create_client_ticket(created, instance, **kwargs) : 
    if created :

        last_ticket_employee = Ticket.objects.filter(is_done=False).order_by('created_at')

        if last_ticket_employee.exists() : 
            last_ticket_employee = last_ticket_employee.last().employee
        else:
            try :
                last_ticket_employee = Ticket.objects.last().employee
            except AttributeError:
                last_ticket_employee = Employee.objects.all()[0]
                ticket = Ticket.objects.create(
                    employee = last_ticket_employee,
                    client = instance,
                )
                ticket.save()
                instance.save()
                return


        employees = Employee.objects.all()
        index = 0
        
        for emp in employees : 
            if emp == last_ticket_employee :
                new_index = index + 1
                if new_index == employees.count() :
                    current_employee = employees[0]
                else:
                    current_employee = employees[new_index]

                break
            index += 1

        ticket = Ticket.objects.create(
            employee = current_employee,
            client = instance,
        )

        ticket.save()
        instance.save()

