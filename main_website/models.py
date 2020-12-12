from django.db import models
# from django.contrib.auth import get_user_model
# Create your models here.
from users.models import MyUser
from dashboard.models import Stalls
from django.db.models import signals
from channels.layers import get_channel_layer
import pdb
from asgiref.sync import async_to_sync



class Message(models.Model):
	author = models.ForeignKey(MyUser,related_name = 'author_messages',on_delete = models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add = True)
	reciever = models.ForeignKey(MyUser,on_delete = models.CASCADE,null= True,blank = True)
	seen_status = models.BooleanField(default = False)
	author_reciever_string = models.CharField(max_length = 20)


	def __str__(self):
		return self.author.mobile

	def last_10_messages(self,author_reciever_string):
		output = Message.objects.order_by('-timestamp').filter(author_reciever_string = author_reciever_string)[:10]
		return output[::-1]


class Notification(models.Model):
	author_reciever_string = models.CharField(max_length = 20)
	reciever = models.ForeignKey(MyUser,on_delete = models.CASCADE,null= True,blank = True,related_name = 'reciever')
	author = models.ForeignKey(MyUser,on_delete = models.CASCADE,null= True,blank = True,related_name = 'author')	
	count = models.IntegerField()

	def notify_clients(self):
	    """
	    Inform client there is a new message.
	    """
	    notification = {
	        'type': 'recieve_group_message',
	        'message': '{}'.format(self.author.id)
	    }

	    channel_layer = get_channel_layer()
	    print("user.id {}".format(self.author))
	    print("user.id {}".format(self.reciever))

	    async_to_sync(channel_layer.group_send)("{}".format('notif_%s' %self.reciever.id), notification)
	    # pdb.set_trace()

	def save(self, *args, **kwargs):
		super(Notification, self).save(*args, **kwargs)
		self.notify_clients()

class Analytics(models.Model):
	page_name = models.CharField(max_length = 50)
	company_name = models.CharField(max_length = 200)
	stall_name = models.CharField(max_length = 200)
	start_time = models.DateTimeField(auto_now_add = True)
	user_id = models.ForeignKey(MyUser,on_delete = models.CASCADE)
	random_string = models.CharField(max_length = 50)
	end_time = models.DateTimeField(null=True,blank = True)


class Question(models.Model):
	user = models.CharField(null=True,blank= True,max_length = 200)
	question = models.TextField()


class ChannelOnlineCount(models.Model):
	author_reciever_string = models.CharField(max_length = 50)
	# company_name = models.CharField()
	count = models.IntegerField()



####newly added
# class social_media_links(models.Model):
#     stall_id = models.ForeignKey(MyUser,on_delete=models.CASCADE)
#     social_id = models.AutoField(primary_key=True,unique=True)
#     youtube = models.CharField(max_length=255,blank=True)
#     twitter = models.CharField(max_length=255,blank=True)
#     facebook = models.CharField(max_length=255,blank=True)
#     linkedin = models.CharField(max_length=255,blank=True)
#     instagram = models.CharField(max_length=255,blank=True)
#     website_url = models.CharField(max_length=255,blank=True)	


class call_schedules(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    stall_id = models.TextField()
    name = models.TextField()
    email = models.CharField(max_length=50,null=True,blank=True)
    mobile = models.CharField(max_length = 30)
    selected_date = models.CharField(max_length=50,null=True,blank=True)
    selected_time = models.CharField(max_length=50,null=True,blank=True)

class partners_tab(models.Model):
	stall_id=models.ForeignKey(MyUser,on_delete=models.CASCADE)
	image=models.ImageField()
	partner_id=models.AutoField(primary_key=True)
	partner_name=models.CharField(max_length=255)


class poll(models.Model):
	question_id = models.AutoField(primary_key=True)
	question = models.TextField()
	option_one = models.CharField(max_length=30,null=True)
	option_two = models.CharField(max_length=30,null=True)
	option_three = models.CharField(max_length=30,null=True)
	option_four = models.CharField(max_length=30,null=True)
	option_one_count = models.IntegerField(default = 0)
	option_two_count = models.IntegerField(default = 0)
	option_three_count = models.IntegerField(default = 0) 
	option_four_count = models.IntegerField(default = 0)
	def total(self):
	    return self.option_one_count + self.option_two_count + self.option_three_count + self.option_four_count	

class Permanent_Poll_Answers(models.Model):
	question_id = models.IntegerField(default=0)
	question = models.TextField()
	option_one_count = models.IntegerField(default = 0)
	option_two_count = models.IntegerField(default = 0)
	option_three_count = models.IntegerField(default = 0) 
	option_four_count = models.IntegerField(default = 0)

# class trest(models.Model):
# 	s = models.CharField(max_length=222)

class another_poll_answers(models.Model):
	question_id = models.IntegerField(default= 0)
	user_id = models.IntegerField(default= 0)


def save_permanent_answer(sender, instance, **kwargs):
	print(sender)
	existing_poll = Permanent_Poll_Answers.objects.filter(question_id = instance.question_id)
	if len(existing_poll) == 0:
		Permanent_Poll_Answers.objects.create(question_id = instance.question_id, question = instance.question,
											option_one_count=instance.option_one_count,
											option_two_count=instance.option_two_count,
											option_three_count=instance.option_three_count,
											option_four_count=instance.option_four_count,
											 )
	else:
		Permanent_Poll_Answers.objects.filter(question_id = instance.question_id).update(
											option_one_count=instance.option_one_count,
											option_two_count=instance.option_two_count,
											option_three_count=instance.option_three_count,
											option_four_count=instance.option_four_count,
		)

	print("Instance Created")

signals.post_save.connect(save_permanent_answer, sender=poll)


class FeedBack(models.Model):
	participants_name = models.CharField(max_length = 50)
	designation = models.CharField(max_length = 50)
	organization = models.CharField(max_length = 50)
	phone = models.CharField(max_length = 50)
	email = models.CharField(max_length = 50)
	question1 = models.CharField(max_length = 50,choices=(('1','1'),('2','2'),('3','3'),('4','4')),default = '1')
	question2 = models.CharField(max_length = 50,choices=(('1','1'),('2','2'),('3','3'),('4','4')),default = '1')
	question3 = models.CharField(max_length = 50,choices=(('1','1'),('2','2'),('3','3'),('4','4')),default = '1')
	question4 = models.CharField(max_length = 50,choices=(('1','1'),('2','2'),('3','3'),('4','4')),default = '1')
	question5 = models.CharField(max_length = 50,choices=(('1','1'),('2','2'),('3','3'),('4','4')),default = '1')
	question6 = models.CharField(max_length = 50,choices=(('1','1'),('2','2'),('3','3'),('4','4')),default = '1')
	question7 = models.CharField(max_length = 50,choices=(('1','1'),('2','2'),('3','3'),('4','4')),default = '1')
	question8 = models.CharField(max_length = 50,choices=(('1','1'),('2','2'),('3','3'),('4','4')),default = '1')
	question9 = models.CharField(max_length = 50,choices=(('0-3 Months','0-3 Months'),('3-6 Months','3-6 Months'),('6-12 Months','6-12 Months')),default = '1')
	question10 = models.TextField()
