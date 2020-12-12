from django.db import models
import random
import string
from users.models import MyUser

days_range = [(str(i),str(i)) for i in range(1,30)]

class OrganizerDetails(models.Model):
	name = models.CharField(max_length = 200,unique=True)
	logo = models.ImageField()
	organizer_chat_link = models.TextField(default="None")
	chat_link = models.TextField(default="None")
	additional_login_field = models.CharField(max_length=20)
	login_page_heading = models.CharField(max_length=20,default='Heading')
	login_page_subheading = models.CharField(max_length=20,default='Sub Heading')

	brand_logo = models.ImageField(null=True,blank = True)

	main_page_background_type = models.CharField(max_length=20,choices=(('image','image'),('video','video')))
	main_page_background_url = models.FileField(null=True,blank = True)
	main_page_front_banner_image = models.FileField(null=True,blank=True)
	
	main_page_back_banner_image1 = models.FileField(null=True,blank=True)
	main_page_back_banner_image2 = models.FileField(null=True,blank=True)
	main_page_back_banner_image3 = models.FileField(null=True,blank=True)
	main_page_back_banner_image4 = models.FileField(null=True,blank=True)
	


	main_page_ppt_image1 = models.FileField(null=True,blank=True)
	main_page_ppt_image2 = models.FileField(null=True,blank=True)
	main_page_ppt_image3 = models.FileField(null=True,blank=True)
	main_page_ppt_image4 = models.FileField(null=True,blank=True)				
	# main_page_slide1 = models.FileField(null=True,blank = True)
	# main_page_slide2 = models.FileField(null=True,blank = True)
	# main_page_slide3 = models.FileField(null=True,blank = True)
	# main_page_slide4 = models.FileField(null=True,blank = True)
	
	lobby_video_link = models.CharField(max_length = 200,null=True,blank = True)
	lobby_background_type = models.CharField(max_length=20,choices=(('image','image'),('video','video')))
	lobby_background_url = models.FileField(null=True,blank = True)
	lobby_left_logo = models.ImageField(null=True,blank = True)
	lobby_right_logo = models.ImageField(null=True,blank = True)
	lobby_banner_link = models.CharField(max_length = 200,null=True,blank = True)
	lobby_banner_image1 = models.ImageField(null=True,blank = True)
	lobby_banner_image2 = models.ImageField(null=True,blank = True)
	lobby_banner_image3 = models.ImageField(null=True,blank = True)
	lobby_banner_image4 = models.ImageField(null=True,blank = True)
	lobby_banner_image5 = models.ImageField(null=True,blank = True)
	lobby_banner_image6 = models.ImageField(null=True,blank = True)
	lobby_banner_image7 = models.ImageField(null=True,blank = True)
	lobby_banner_image8 = models.ImageField(null=True,blank = True)
	hall_title_1 = models.CharField(max_length = 200,null=True,blank = True)
	hall_title_2 = models.CharField(max_length = 200,null=True,blank = True)
	hall_title_3 = models.CharField(max_length = 200,null=True,blank = True)
	hall_title_4 = models.CharField(max_length = 200,null=True,blank = True)

	resource_1_name = models.CharField(max_length = 200,null=True,blank = True)
	resource_1_link = models.CharField(max_length = 200,null=True,blank = True)
	resource_2_name = models.CharField(max_length = 200,null=True,blank = True)
	resource_2_link = models.CharField(max_length = 200,null=True,blank = True)
	resource_3_name = models.CharField(max_length = 200,null=True,blank = True)
	resource_3_link = models.CharField(max_length = 200,null=True,blank = True)	
	resource_4_name = models.CharField(max_length = 200,null=True,blank = True)
	resource_4_link = models.CharField(max_length = 200,null=True,blank = True)	

	auditorium_youtube_name = models.CharField(max_length = 200,null=True,blank = True)	
	auditorium_keynote_track = models.CharField(max_length = 200,null=True,blank = True)
	auditorium_background_image = models.ImageField(null=True,blank = True)

	auditorium_video_type = models.CharField(max_length = 50,null=True,blank = True,choices = (('youtube','youtube'),('zoom','zoom')),default = 'youtube')

	info_desk = models.CharField(max_length = 200,null=True,blank = True)
	website_url = models.CharField(max_length = 200,null=True,blank = True)
	info_background_image = models.ImageField(null=True,blank = True)
	infocenter_video = models.CharField(max_length = 200,null=True,blank = True)
	infocenter_doc = models.TextField(null=True,blank=True)
	infocenter_left_banner  = models.ImageField(null=True,blank = True)
	infocenter_right_banner = models.ImageField(null=True,blank = True)
	hall_logo_left = models.ImageField(null=True,blank = True)
	hall_logo_center = models.ImageField(null=True,blank = True)
	hall_logo_right = models.ImageField(null=True,blank = True)
	hall_background_image = models.ImageField(null=True,blank = True)

	resource_ui_name = models.CharField(max_length = 200,null=True,blank = True)
	social_lounge_name = models.CharField(max_length = 200,null=True,blank = True)
	social_lounge_background_image = models.ImageField(null=True,blank = True)


	validity_time = models.CharField(max_length=5,choices = days_range,null=True,blank = True)

	zoom_meeting_id = models.CharField(max_length = 15,null=True,blank = True)
	zoom_password = models.CharField(max_length = 15,null=True,blank = True)

	login_url = models.CharField(max_length = 20,null=True,blank = True)
	login_background_image = models.ImageField(upload_to = 'dashboard')
        

class Stalls(models.Model):
	organization = models.ForeignKey(OrganizerDetails,on_delete = models.CASCADE)
	stall_video_url = models.CharField(max_length = 200)
	stall_web_link = models.CharField(max_length=200)

	username = models.CharField(max_length=255,default="stall owner")


	stall_admin_link = models.CharField(max_length = 200,null=True,blank = True)
	stall_image_link = models.ImageField(null=True,blank = True)#(max_length=200)	
	stall_doc_url = models.FileField(null=True,blank = True)
	stall_front_image = models.ImageField(null=True,blank=True)
	unique_url = models.CharField(max_length=50,null=True,blank = True)
	stall_first_rotating_image = models.ImageField(null=True,blank = True)
	stall_second_rotating_image = models.ImageField(null=True,blank = True)
	stall_third_rotating_image = models.ImageField(null=True,blank = True)
	stall_fourth_rotating_image = models.ImageField(null=True,blank = True)
	stall_whatsapp_number = models.CharField(max_length = 20,null=True,blank = True)
	youtube = models.CharField(null=True,max_length=255,blank=True)
	twitter = models.CharField(null=True,max_length=255,blank=True)
	facebook = models.CharField(null=True,max_length=255,blank=True)
	linkedin = models.CharField(null=True,max_length=255,blank=True)
	instagram = models.CharField(null=True,max_length=255,blank=True)

	def save(self, *args, **kwargs):
		if self.unique_url:
			pass
		else:			
			self.unique_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 25))
			self.stall_admin_link = self.unique_url
			MyUser.objects.create_staff_user(self.unique_url,self.username)
		super(Stalls, self).save(*args, **kwargs)




class StallZoom(models.Model):
	stall_id = models.ForeignKey(Stalls,on_delete = models.CASCADE)
	zoom_meeting_id = models.CharField(max_length = 20,null=True,blank = True)
	zoom_meeting_password = models.CharField(max_length = 20,null=True,blank = True)


class EventStallUsers(models.Model):
	event_stall_id = models.ForeignKey(Stalls,on_delete=models.CASCADE)
	organizer_name = models.ForeignKey(OrganizerDetails,on_delete=models.CASCADE)
	event_user_id = models.IntegerField()


class Stall_Owner_documents(models.Model):
	# document_id = models.AutoField(primary_key = True)
	stall_id = models.TextField()
	document_types = [
		('V',"Video"),
		('D','Document')
	]
	document_type = models.CharField(max_length=2,choices = document_types)
	document_title = models.TextField(null=True)
	document_description = models.TextField(null=True)
	document_link = models.TextField()

class Stall_Sales_Representatives(models.Model):
	stall_id = models.TextField()
	name = models.TextField()
	email = models.TextField()
	mobile = models.TextField()
	designation = models.TextField()