from django.db import models


class State(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LocalGovernmentArea(models.Model):
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['state']


'''to load the various local governments via a text file'''
# record = []
# with open(r'C:\Users\ADEBAYO VICTOR\ANIMAL MANAGER\location\local_zamfara.txt', 'r') as f:
#     for thing in f:
#         record.append(thing.strip('\n'))
#     print(record)
#
# for thing in record:
#     queryset = LocalGovernmentArea.objects.create(state=State.objects.get(id=37), name=f'{thing}')
#     queryset.save()
