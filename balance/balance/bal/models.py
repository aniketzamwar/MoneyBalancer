from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Transaction(models.Model):
    trans_amount = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='Amount')
    trans_date = models.DateField(verbose_name='Date of Transaction')
    trans_name = models.CharField(max_length = 10,verbose_name='Title')
    trans_description = models.CharField(max_length = 150,verbose_name='Description')
    paidby = models.ForeignKey(User,verbose_name='Name')
    amount = models.DecimalField(max_digits=7, decimal_places=2,verbose_name='Shared Amount')
    def __unicode__(self):
        return u'%s, %s, $%s, %s' %(self.trans_name, self.trans_description, str(self.trans_amount),str(self.trans_date))
    
class Balancer(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2,verbose_name='Shared Amount')
    trans = models.ForeignKey(Transaction,verbose_name='Transaction')
    trans_member = models.ForeignKey(User,verbose_name='Member of Transaction')
    
    def __unicode__(self):
        return u'%s %s: %f' %(self.trans_member.first_name,self.trans_member.last_name,self.amount)

class Comments(models.Model):
    commenter = models.ForeignKey(User)
    trans = models.ForeignKey(Transaction)
    comment = models.CharField(max_length = 100)

class Frelation(models.Model):
    a_user = models.ForeignKey(User,related_name="a_user")
    friend_with = models.ForeignKey(User,related_name="friend_with")
