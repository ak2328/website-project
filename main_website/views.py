from django.shortcuts import render
from dashboard.models import OrganizerDetails, EventStallUsers, Stalls, StallZoom, Stall_Owner_documents,Stall_Sales_Representatives
from users.decorators import user_authorized_for_page
from django.urls import reverse_lazy
import hashlib
import hmac
import base64
import time
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from users.models import MyUser
from .models import Notification, Analytics, Permanent_Poll_Answers
import urllib.parse
# from django.http import JsonResponse
from .models import Question, poll, another_poll_answers
import pdb
from .models import Message
from users.models import MyUser
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from main_website.forms import FeedbackForm
from django.views.generic import CreateView
# Create your views here.

def calculate_registered_users(organizer):
    # organizer = OrganizerDetails.objects.get(name = company_name)
    return EventStallUsers.objects.filter(organizer_name=organizer).count()


def hall_array(organizer_details):
    return [organizer_details.hall_title_1, organizer_details.hall_title_2, organizer_details.hall_title_3,
            organizer_details.hall_title_4]


def question(request):
    question = request.GET.get('question', None)
    Question.objects.create(question=question, user=MyUser.objects.get(id=request.user.id).name)
    return JsonResponse({'success': 'success'})


#@user_authorized_for_page
def home_page(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    background_type = organizer_details.main_page_background_type
    background_url = organizer_details.main_page_background_url
    lobby_page_url = '127.0.0.1:8000/lobby/' + company_name + stall_text

    event_stall_users = EventStallUsers.objects.filter(organizer_name=organizer_details)
    user_ids = [i.event_user_id for i in event_stall_users]

    users = MyUser.objects.filter(id__in=user_ids).order_by('name')

    resource_links = [[organizer_details.resource_1_name, organizer_details.resource_1_link],
                      [organizer_details.resource_2_name, organizer_details.resource_2_link],
                      [organizer_details.resource_3_name, organizer_details.resource_3_link],
                      [organizer_details.resource_4_name, organizer_details.resource_4_link]]

    slides = [organizer_details.main_page_ppt_image1, organizer_details.main_page_ppt_image2,
              organizer_details.main_page_ppt_image3, organizer_details.main_page_ppt_image4]
    notifications_array,users_array = get_chats(requests,organizer_details)
    users_chat = zip(notifications_array, users_array)

    context = {
        'background_type': background_type,
        'banner_links': resource_links,
        'background_url': background_url,
        'lobby_page_url': lobby_page_url,
        'company_name': company_name,
        'stall_text': stall_text,
        'registered_users': calculate_registered_users(organizer_details),
        'main_page_front_banner_image': organizer_details.main_page_front_banner_image,
        
        'main_page_back_banner_image1': organizer_details.main_page_back_banner_image1,
        'main_page_back_banner_image2': organizer_details.main_page_back_banner_image2,
        'main_page_back_banner_image3': organizer_details.main_page_back_banner_image3,
        'main_page_back_banner_image4': organizer_details.main_page_back_banner_image4,
        
        'slides': slides,
        'hall_array': hall_array(organizer_details),
        'users':users,
        'users_chat':users_chat,
        'current_user': MyUser.objects.get(id=requests.user.id),        
    }

    # return render(requests, 'main_website/main_page.html', context)
    return render(requests, 'new/main_page.html', context)


# @user_authorized_for_page
def lobby_page(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    hall_titles = [organizer_details.hall_title_1, organizer_details.hall_title_2, organizer_details.hall_title_3,
                   organizer_details.hall_title_4]
    resource_links = [[organizer_details.resource_1_name, organizer_details.resource_1_link],
                      [organizer_details.resource_2_name, organizer_details.resource_2_link],
                      [organizer_details.resource_3_name, organizer_details.resource_3_link],
                      [organizer_details.resource_4_name, organizer_details.resource_4_link]]
    lobby_left_logo = organizer_details.lobby_left_logo
    lobby_right_logo = organizer_details.lobby_right_logo
    lobby_video_link = organizer_details.lobby_video_link
    lobby_background_url = organizer_details.lobby_background_url
    lobby_banner_link = organizer_details.lobby_banner_link
    back_button = '/arena/homepage/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)

    event_stall_users = EventStallUsers.objects.filter(organizer_name=organizer_details)
    user_ids = [i.event_user_id for i in event_stall_users]

    users = MyUser.objects.filter(id__in=user_ids).order_by('name')

    ### need to remove ####
    stalls = Stalls.objects.filter(organization=organizer_details)
    stall_texts = [i.unique_url for i in stalls]
    lobby_banner_images_left = [organizer_details.lobby_banner_image1, organizer_details.lobby_banner_image2,
                                organizer_details.lobby_banner_image3, organizer_details.lobby_banner_image4]
    lobby_banner_images_right = [organizer_details.lobby_banner_image5, organizer_details.lobby_banner_image6,
                                 organizer_details.lobby_banner_image7, organizer_details.lobby_banner_image8]

    notifications_array,users_array = get_chats(requests,organizer_details)
    users_chat = zip(notifications_array, users_array)

    context = {
        'hall_titles': hall_titles,
        'banner_links': resource_links,
        'lobby_left_logo': lobby_left_logo,
        'lobby_right_logo': lobby_right_logo,
        'lobby_video_link': lobby_video_link,
        'lobby_background_type': organizer_details.lobby_background_type,
        'lobby_background_url': lobby_background_url,
        'company_name': company_name,
        'stall_text': stall_text,
        'lobby_banner_link': lobby_banner_link,
        'registered_users': calculate_registered_users(organizer_details),
        'stall_texts': stall_texts,
        'back_button': back_button,
        'hall_array': hall_array(organizer_details),
        'lobby_banner_images_left': lobby_banner_images_left,
        'lobby_banner_images_right': lobby_banner_images_right,
        'users':users,
        'users_chat':users_chat,
        'current_user': MyUser.objects.get(id=requests.user.id),
    }

    # return render(requests, 'main_website/lobby_page.html', context)
    return render(requests, 'new/lobby_page.html', context)


# @user_authorized_for_page
def auditorium(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    auditorium_background_image = organizer_details.auditorium_background_image
    polls = poll.objects.all()
    current_user_status = False
    poll_result = []
    if len(polls) == 0:
        pass
    else:
        poll_result = [polls[0].option_one_count, polls[0].option_two_count, polls[0].option_three_count, polls[0].option_four_count ]
        poll_answers = another_poll_answers.objects.all()
        print("Poll Answers are  ",poll_answers)
        question_id = polls[0].question_id
        for i in poll_answers:
            if i.user_id == requests.user.id and i.question_id == question_id:
                current_user_status = True
                break
    
    if organizer_details.auditorium_video_type == 'youtube':
        
        auditorium_youtube_name = organizer_details.auditorium_youtube_name
        auditorium_keynote_track = organizer_details.auditorium_keynote_track
        back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
        back_button = urllib.parse.quote(back_button)

        notifications_array,users_array = get_chats(requests,organizer_details)
        users_chat = zip(notifications_array, users_array)
        context = {
            'auditorium_background_image': auditorium_background_image,
            'auditorium_keynote_track': auditorium_keynote_track,
            'auditorium_youtube_name': auditorium_youtube_name,
            'company_name': company_name,
            'stall_text': stall_text,
            'registered_users': calculate_registered_users(organizer_details),
            'back_button': back_button,
            'hall_array': hall_array(organizer_details),
            'users_chat':users_chat,
            'current_user': MyUser.objects.get(id=requests.user.id),    
            'polls' : polls,  
            'poll_status':current_user_status,
            'poll_result':poll_result
        }
        print("this is auditorium ")
        # return render(requests, 'main_website/auditorium.html', context)
        return render(requests, 'new/auditorium.html', context)
    else:
        zoom_id = organizer_details.zoom_meeting_id
        zoom_password = organizer_details.zoom_password

        back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
        back_button = urllib.parse.quote(back_button)

        context = {
            'auditorium_background_image': auditorium_background_image,        
            'company_name': company_name,
            'stall_text': stall_text,
            'registered_users': calculate_registered_users(organizer_details),
            'zoom_meeting_id': zoom_id,
            'zoom_meeting_password': zoom_password,
            'back_button': back_button,
            'hall_array': hall_array(organizer_details),
            'polls' : polls,
            'poll_status':current_user_status,
            'poll_result':poll_result
        }
        print("this is auditorium zoom")
        # return render(requests, 'main_website/auditorium_zoom.html', context)
        return render(requests, 'new/auditorium_zoom.html', context)
        # return render(requests, 'new/auditorium_zoom.html', context)


# @user_authorized_for_page
def info_desk(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)
    infocenter_video = organizer_details.infocenter_video
    infocenter_doc = organizer_details.infocenter_doc
    infocenter_left = organizer_details.infocenter_left_banner
    infocenter_right = organizer_details.infocenter_right_banner
    infocenter_background_image = organizer_details.info_background_image
    chat_link = organizer_details.chat_link
    notifications_array,users_array = get_chats(requests,organizer_details)
    users_chat = zip(notifications_array, users_array)
    
    context = {
        'company_name': company_name,
        'stall_text': stall_text,
        'organizer_details': organizer_details,
        'registered_users': calculate_registered_users(organizer_details),
        'back_button': back_button,
        'hall_array': hall_array(organizer_details),
        'infocenter_video': infocenter_video,
        'infocenter_doc': infocenter_doc,
        'infocenter_left': infocenter_left,
        'infocenter_right': infocenter_right,
        'infocenter_background_image':infocenter_background_image,
        'users_chat':users_chat,
        "chat_link":chat_link,
        'current_user': MyUser.objects.get(id=requests.user.id),

    }
    return render(requests, 'new/infocenter.html', context)


#@user_authorized_for_page
def exhibit_hall(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    logo_left = organizer_details.hall_logo_left
    logo_center = organizer_details.hall_logo_center
    logo_right = organizer_details.hall_logo_right
    background_image = organizer_details.hall_background_image
    stalls = Stalls.objects.filter(organization=organizer_details)
    stall_images = [i.stall_front_image for i in stalls]
    stall_texts = [i.unique_url for i in stalls]
    back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)
    text = stall_texts

    event_stall_users = EventStallUsers.objects.filter(organizer_name=organizer_details)
    user_ids = [i.event_user_id for i in event_stall_users]

    users = MyUser.objects.filter(id__in=user_ids).order_by('name')

    notifications_array,users_array = get_chats(requests,organizer_details)
    users_chat = zip(notifications_array, users_array)

    context = {
        'company_name': company_name,
        'stall_text': stall_text,
        'logo_left': logo_left,
        'logo_center': logo_center,
        'logo_right': logo_right,
        'background_image': background_image,
        # 'stall_images': stall_images,
        'registered_users': calculate_registered_users(organizer_details),
        'text': text,
        'back_button': back_button,
        'hall_array': hall_array(organizer_details),
        'users':users,
        'users_chat':users_chat,
        'current_user': MyUser.objects.get(id=requests.user.id),        

    }
    return render(requests, 'new/exhibit_hall.html', context)
    # return render(requests, 'main_website/expohall.html', context)


def auditorium_owner(requests, company_name):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    context = {
    }
    return render(requests, 'main_website/auditorium_owner.html', context)


@user_authorized_for_page
def resource_center(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    return render(requests, 'main_website/resource_center.html', context)


from django.shortcuts import render
from .models import *

def get_chats(request,organizer_details,restrict = False):
    user_id = request.user.id
    all_messages = Message.objects.filter(Q(reciever = user_id) | Q(author = user_id)).order_by('-timestamp')
    # identify unique messages to know people
    existing_author_ids, item_ids = [], []
    existing_authors = []
    existing_author_names = []
    for item in all_messages:
        if item.author_reciever_string not in item_ids:
            if (item.reciever != None) &(item.author != None):
                if item.author.id == user_id:
                    existing_author_ids.append(item.reciever.id)
                    existing_authors.append(item.reciever)
                    # existing_author_names.append(MyUser.objects.get(id = item.reciever.id).designation)
                else:
                    existing_author_ids.append(item.author.id)
                    existing_authors.append(item.author)
                item_ids.append(item.author_reciever_string)    

    existing_author_ids.append(user_id)
    if restrict:
        event_users_ids = []
    else:
        event_users_ids = EventStallUsers.objects.filter(organizer_name=organizer_details).values('event_user_id')

    remaining_users = MyUser.objects.exclude(id__in=existing_author_ids).filter(id__in = event_users_ids).order_by('name')
    # remaining_users  = 
    existing_author_ids.remove(user_id)
    notifications_count_array = []
    for author_id in existing_author_ids:
        total_unread_message = Notification.objects.filter(reciever = user_id,author = author_id).count()
        notifications_count_array.append(total_unread_message)

    existing_authors.extend(remaining_users)
    notifications_count_array.extend([0]*remaining_users.count())
    return notifications_count_array,existing_authors



#@user_authorized_for_page
def social_lounge(requests, company_name, stall_text):
    
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    notifications_array,users_array = get_chats(requests,organizer_details)
    users = zip(notifications_array, users_array)

    room_name = 'wow'
    back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)
    context = {
        'company_name': company_name,
        'stall_text': stall_text,
        'registered_users': calculate_registered_users(organizer_details),
        'room_name': room_name,
        'users': users,
        'current_user': MyUser.objects.get(id=requests.user.id),
        'back_button': back_button,
        'hall_array': hall_array(organizer_details),
        'background_image': organizer_details.social_lounge_background_image
    }
    # return render(requests, 'main_website/social_lounge.html', context)
    return render(requests, 'new/social_lounge.html', context)


def generateSignature(data):
    ts = int(round(time.time() * 1000)) - 30000;
    print(data)
    msg = data['apiKey'] + str(data['meetingNumber']) + str(ts) + str(data['role']);
    message = base64.b64encode(bytes(msg, 'utf-8'));
    # message = message.decode("utf-8");
    secret = bytes(data['apiSecret'], 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256);
    hash = base64.b64encode(hash.digest());
    hash = hash.decode("utf-8");
    tmpString = "%s.%s.%s.%s.%s" % (data['apiKey'], str(data['meetingNumber']), str(ts), str(data['role']), hash);
    signature = base64.b64encode(bytes(tmpString, "utf-8"));
    signature = signature.decode("utf-8");
    return signature.rstrip("=");


@user_authorized_for_page
def stall(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    stall_id = Stalls.objects.get(unique_url=stall_text)
    stall_zoom = StallZoom.objects.get(stall_id=stall_id)

    back_button = '/arena/stall_details/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)

    context = {
        'company_name': company_name,
        'stall_text': stall_text,
        'registered_users': calculate_registered_users(organizer_details),
        'zoom_meeting_id': stall_zoom.zoom_meeting_id,
        'zoom_meeting_password': stall_zoom.zoom_meeting_password,
        'back_button': back_button,
        'hall_array': hall_array(organizer_details)
    }
    # return render(requests, 'main_website/zoom.html', context)
    return render(requests, 'new/zoom.html', context)


def stall_iframe(requests):
    return render(requests, 'main_website/meeting.html')


def zoom_start(requests):
    data = {'apiKey': "nrMRNKkOTLCOJWBeQIPKZw",
            'apiSecret': "uapXKfPU5xLQqocbJjm3vfzQAsJ3gWdO6MmC",
            'meetingNumber': requests.GET.get('meetingNumber', None),
            'role': 0
            }
    return JsonResponse({'signature': generateSignature(data)})


def stall_portal(requests, company_name, stall_text):
    stall = Stalls.objects.get(unique_url=stall_text)
    context = {}
    zoom = None
    if requests.POST:
        try:
            zoom = StallZoom.objects.get(stall_id=stall)
            zoom.zoom_meeting_id = requests.POST['zoom_meeting_id']
            zoom.zoom_meeting_password = requests.POST['zoom_meeting_password']
            zoom.save()
            messages.success(requests, "Successfully Submitted")
        except:
            zoom = StallZoom()
            zoom.stall_id = stall
            zoom.zoom_meeting_id = requests.POST['zoom_meeting_id']
            zoom.zoom_meeting_password = requests.POST['zoom_meeting_password']
            zoom.save()
            messages.success(requests, "Successfully Submitted")
    else:
        try:
            zoom = StallZoom.objects.get(stall_id=stall)
        except:
            context = {}
    try:
        context['zoom_meeting_id'] = zoom.zoom_meeting_id
        context['zoom_meeting_password'] = zoom.zoom_meeting_password
    except:
        pass
    context['company_name'] = company_name
    context['stall_text'] = stall_text
    return render(requests, 'main_website/stall_member.html', context)



def stall_details(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)

    stall = Stalls.objects.get(unique_url=stall_text)
    stall_web_link = stall.stall_web_link
    stall_video_url = stall.stall_video_url
    stall_doc_url = stall.stall_doc_url
    stall_whatsapp_number = stall.stall_whatsapp_number
    stall_image_background = stall.stall_image_link
    back_button = '/arena/exhibit_hall/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)
    rotating_images = None

    stall_documents_data = Stall_Owner_documents.objects.filter(stall_id=stall_text)
    representative_data = Stall_Sales_Representatives.objects.filter(stall_id = stall_text)
    document_id = []
    document_title = []
    document_links = []
    video_id = []
    video_title = []
    video_links = []
    sales_representatives = []
    for data in stall_documents_data:
        if data.document_type == 'V':
            video_id.append(data.id)
            video_title.append(data.document_title)
            video_links.append(data.document_link)
        elif data.document_type == 'D':
            document_id.append(data.id)
            document_title.append(data.document_title)
            document_links.append(data.document_link)

    for data in representative_data:
        sales_representatives.append([data.name, data.email, data.mobile, data.designation])

    document=list(zip(document_id,document_title,document_links))
    video = list(zip(video_id,video_title,video_links))

    if stall.stall_first_rotating_image:
        rotating_images = [stall.stall_first_rotating_image, stall.stall_second_rotating_image,
                           stall.stall_third_rotating_image, stall.stall_fourth_rotating_image, ]
    else:
        rotating_images = None

    zoom_id = None
    zoom_password = None

    try:
        stall_zoom = StallZoom.objects.get(stall_id=stall_id)
        zoom_id = stall_zoom.zoom_meeting_id
        zoom_password = stall_zoom.zoom_meeting_password
    except:
        pass

    notifications_array,users_array = get_chats(requests,organizer_details)
    users_chat = zip(notifications_array, users_array)
    
    # notifications_array,users_array = get_chats(requests,organizer_details)
    owner_chat = zip([0], MyUser.objects.filter(mobile = stall_text))

    context = {
        'company_name': company_name,
        'stall_text': stall_text,
        'stall_web_link': stall_web_link,
        'stall_video_url': stall_video_url,
        'stall_doc_url': stall_doc_url,
        'background': stall_image_background,
        'registered_users': calculate_registered_users(organizer_details),
        'back_button': back_button,
        'hall_array': hall_array(organizer_details),
        'rotating_images': rotating_images,
        'stall_whatsapp_number': stall_whatsapp_number,
        'zoom_meeting_id': zoom_id,
        'zoom_meeting_password': zoom_password,        
        'users_chat':users_chat,
        'current_user': MyUser.objects.get(id=requests.user.id),
        'owner_chat':owner_chat,
        'stall_documents':document,
        'stall_videos':video,
        "sales_representatives":sales_representatives 
    }


    return render(requests, 'new/stall_details_page.html', context)

def userwise_notification(users, notifications):
    users_array = []
    notifications_array = []

    for user in users:
        flag = 0
        for notification in notifications:
            if notification.author.id == user.id:
                notifications_array.append(notification.count)
                users_array.append(user)
                flag = 1
        if (flag == 0):
            notifications_array.append(0)
            users_array.append(user)

    for i in range(len(notifications_array)):
        for j in range(i + 1, len(notifications_array)):
            if (notifications_array[i] <= notifications_array[j]):
                temp = notifications_array[i]
                notifications_array[i] = notifications_array[j]
                notifications_array[j] = temp

                temp = users_array[i]
                users_array[i] = users_array[j]
                users_array[j] = temp

    users = zip(notifications_array, users_array)
    return users


def stall_user_chat(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    stall = Stalls.objects.get(unique_url=stall_text)

    users = MyUser.objects.filter(username=stall_text)

    notifications = Notification.objects.filter(reciever=requests.user)
    users = userwise_notification(users, notifications)

    room_name = 'wow'
    context = {
        'company_name': company_name,
        'stall_text': stall_text,
        'registered_users': calculate_registered_users(organizer_details),
        'room_name': room_name,
        'users': users,
        'current_user': MyUser.objects.get(id=requests.user.id),
        # 'notifications':Notifications
    }

    return render(requests, 'main_website/stall_chat.html', context)


def stall_owner_chat(requests, company_name, stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)

    notifications_array,users_array = get_chats(requests,organizer_details,restrict = True)
    users = zip(notifications_array, users_array)

    room_name = 'wow'
    back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)
    context = {
        'company_name': company_name,
        'stall_text': stall_text,
        'registered_users': calculate_registered_users(organizer_details),
        'room_name': room_name,
        'users': users,
        'users_chat':users,
        'current_user': MyUser.objects.get(id=requests.user.id),
        'back_button': back_button,
        'hall_array': hall_array(organizer_details),
        'background_image': organizer_details.social_lounge_background_image
    }

    return render(requests, 'main_website/stall_owner_chat.html', context)


def stall_owner_page(request, company_name, stall_text):
    stall_user_id = MyUser.objects.get(id=request.user.id).mobile

    context = {
        'company_name': company_name,
        'stall_text': stall_text,
        'registered_users': calculate_registered_users(organizer_details),
        'room_name': room_name,
        'users': users,
        'current_user': MyUser.objects.get(id=request.user.id),
        # 'notifications':Notifications
    }
    return render(request, 'main_website/stall_owner.html', context)

def photobooth(request):
    return render(request,'new/photobooth.html')



def stall_analytics(request, company_name, stall_text):
    ######CHECK for stall owner authentications
    """
        send data to dashboard from stall
    """
    # stall_user_id = MyUser.objects.get(id=request.user.id).mobile
    # stall_social_media_links = social_media_links.objects.filter(stall_id=stall_text)
    stall_analytics_data,schedules_calls_data = [],[]
    stall = Stalls.objects.get(unique_url=stall_text)
    stall_unique_id = stall.id
    links = {
        'youtube':stall.youtube,
        'twitter':stall.twitter,
        'facebook':stall.facebook,
        'linkedin':stall.linkedin,
        'instagram':stall.instagram,
        'website_url':stall.stall_web_link
    }
    # get data from schedule call
    print('count0')
    schedule_calls = call_schedules.objects.filter(stall_id=stall_text)
    print(schedule_calls)
    if len(schedule_calls) != 0:
        for call in schedule_calls:
            user_mob = call.mobile
            user_email = MyUser.objects.get(mobile=user_mob).email
            schedules_calls_data.append([call.name,user_mob ,user_email ,call.selected_date, call.selected_time])
    else:
        schedules_calls_data.append(["",0,"",""])
    # print(schedules_calls_data)
    print('count1')
    # Analytics Code Begins Here
    analytics_data = Analytics.objects.filter(stall_name = stall_text)
    users_list = Analytics.objects.filter(stall_name = stall_text).values('user_id').distinct()
    visitors_list = []
    users_dict = {}
    for user in users_list:
        # try:
        #     users_dict[user]
        data = Analytics.objects.filter(user_id = MyUser.objects.get(id = user['user_id'])).first()
        mobile = data.user_id
        temp_data = MyUser.objects.get(mobile = mobile)
        name, email = temp_data.name,temp_data.email
        if mobile not in visitors_list:
            visitors_list.append(mobile)
        stall_analytics_data.append([name,mobile ,email, data.start_time, data.end_time])
        # except:
        #     users_dict[user] = 1
    print('count2')
    # stall_analytics_data.reverse()
    schedules_calls_data.reverse()

    users = analytics_data.distinct('user_id')
    print('count3')
    context = {
        "company_name":company_name,
        "social_media_links":links,
        "total_visitors":len(visitors_list),
        "active_users":0,
        "document_downloads_count":0,
        "document_views_count":0,
        "video_views":0,
        "stall_analytics":stall_analytics_data,
        "schedule_call":schedules_calls_data,
        "stall_text":stall_text,
        "users":stall_analytics_data
        }

    print("Data is ",context["schedule_call"])
    return render(request,'main_website/stall_dashboard.html',context)  

def stall_add_documents(request, company_name, stall_text):
    owner_documents = Stall_Owner_documents.objects.filter(stall_id = stall_text)
    all_documents = []
    for data in owner_documents:
        all_documents.append([
            data.id,
            data.document_type, 
            data.document_title,
            data.document_description, 
            data.document_link
          ])
    social_media_links_data = Stalls.objects.filter(unique_url = stall_text)
    links = [
        social_media_links_data[0].youtube,
        social_media_links_data[0].twitter,
        social_media_links_data[0].facebook,
        social_media_links_data[0].linkedin,
        social_media_links_data[0].instagram
        ]
    all_documents.reverse()
    context={
            'social_media_links':links,
            'documents':all_documents,
            "stall_text":stall_text,
            "company_name":company_name
            }

    return render(request,'main_website/add_Documents.html',context) 



class FeeBack(CreateView):
    template_name = 'main_website/feedback_form.html'
    form_class = FeedbackForm
    def form_valid(self,form):
        return  HttpResponse('<h1> Thanks for Your FeedBack </h1>')


def stall_add_sales_representatives(request, company_name, stall_text):
    stall_data = Stall_Sales_Representatives.objects.filter(stall_id = stall_text)
    sales_representative_data = []
    for data in stall_data:
        sales_representative_data.append([
            data.id , data.name, data.email, data.mobile, data.designation
        ])
    sales_representative_data.reverse()
    context={
            'sales_representative':sales_representative_data,
            "stall_text":stall_text,
            "company_name":company_name}
    return render(request,"main_website/sales_representative.html",context)          


def first_floor(request,company_name,stall_text):


    organizer_details = OrganizerDetails.objects.get(name=company_name)
    back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)
    context = {
               'company_name':company_name,
               'stall_text':stall_text,
               'hall_array': hall_array(organizer_details),
               'back_button': back_button
    }

    return render(request,"new/first_floor/first_floor.html",context)

def first_floor_link1(request,company_name,stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)
    context = {
               'company_name':company_name,
               'stall_text':stall_text,
               'hall_array': hall_array(organizer_details),
               'back_button': back_button
    }

    return render(request,"new/first_floor/first_floor_link1.html",context)

def first_floor_link2(request,company_name,stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)
    context = {
               'company_name':company_name,
               'stall_text':stall_text,
               'hall_array': hall_array(organizer_details),
               'back_button': back_button
    }
    return render(request,"new/first_floor/first_floor_link2.html",context)

def first_floor_link3(request,company_name,stall_text):
    organizer_details = OrganizerDetails.objects.get(name=company_name)
    back_button = '/arena/lobby/' + company_name + '/' + stall_text + '/'
    back_button = urllib.parse.quote(back_button)
    context = {
               'company_name':company_name,
               'stall_text':stall_text,
               'hall_array': hall_array(organizer_details),
               'back_button': back_button
    }
    return render(request,"new/first_floor/first_floor_link3.html",context)
    


# def vote(request, poll_id):
#     poll = poll.objects.get(pk=poll_id)

#     if request.method == 'POST':

#         selected_option = request.POST['poll']
#         if selected_option == 'option1':
#             poll.option_one_count += 1
#         elif selected_option == 'option2':
#             poll.option_two_count += 1
#         elif selected_option == 'option3':
#             poll.option_three_count += 1
#         else:
#             return HttpResponse(400, 'Invalid form option')
    
#         poll.save()

#         return redirect('results', poll.id)

#     context = {
#         'poll' : poll
#     }
#     return render(request, 'poll/vote.html', context)


def submit_polling_results(request,company_name, stall_text):
    print("Values inside POST Method is ",request.POST)
    submitted_option = request.POST['options']
    current_user = request.user.id
    print("this is >question id",request.POST["question_id"])
    question_id = request.POST["question_id"]
    try:
        poll_data=poll.objects.get(question_id=question_id)
        permanent_poll_data = Permanent_Poll_Answers.objects.get(question_id = question_id)


        if poll_data.option_one == submitted_option:
            poll_data.option_one_count=poll_data.option_one_count+1
            permanent_poll_data.option_one_count=permanent_poll_data.option_one_count+1
        elif poll_data.option_two == submitted_option:
            poll_data.option_two_count=poll_data.option_two_count+1
            permanent_poll_data.option_two_count=permanent_poll_data.option_two_count+1
        elif poll_data.option_three == submitted_option:
            poll_data.option_three_count=poll_data.option_three_count+1
            permanent_poll_data.option_three_count=permanent_poll_data.option_three_count+1
        elif poll_data.option_four == submitted_option:
            poll_data.option_four_count=poll_data.option_four_count+1  
            permanent_poll_data.option_four_count=permanent_poll_data.option_four_count+1

        permanent_poll_data.save()
        poll_data.save()
        all_data = another_poll_answers.objects.filter(question_id=question_id)
        print("all Data is ",all_data)
        if len(all_data) == 0:
            another_poll_answers.objects.create(question_id=question_id,user_id=current_user)
        for data in all_data:
            if data.user_id == current_user:
                continue
            else:
                another_poll_answers.objects.create(question_id=question_id,user_id=current_user)   
        print("thisisii>>>>",company_name,stall_text)
    except Exception as e:
        return HttpResponseRedirect(f"/arena/auditorium/{company_name}/{stall_text}/")
    return HttpResponseRedirect(f"/arena/auditorium/{company_name}/{stall_text}/")


def update_document(request,company_name,stall_text):
    doc_id = request.POST['document_id']
    doc_title = request.POST['title']
    link = request.POST['link']
    description = request.POST['description']

    Stall_Owner_documents.objects.filter(id=doc_id).update(document_title = doc_title,
                                            document_link= link,
                                            document_description = description )

    return HttpResponseRedirect(f"/arena/stall_add_documents/{company_name}/{stall_text}/")
     #Redirect to Stall Dashboard URL  

def update_social_media_link(request, company_name, stall_text):
    media = request.POST['social']
    link = request.POST['link']
    if media=="youtube":
        data = Stalls.objects.get(unique_url = stall_text)
        data.youtube = link
    elif media=="linkedin":
        data = Stalls.objects.get(unique_url = stall_text)
        data.linkedin=link
    elif media=="facebook":
        data = Stalls.objects.get(unique_url = stall_text)
        data.facebook=link
    elif media=="twitter":
        data = Stalls.objects.get(unique_url = stall_text)
        data.twitter=link
    elif media=="insta":
        data = Stalls.objects.get(unique_url = stall_text)
        data.instagram=link
    data.save()
    return HttpResponseRedirect(f"/arena/stall_add_documents/{company_name}/{stall_text}/")


def new_document(request, company_name, stall_text):
    new_title = request.POST['title']
    new_link = request.POST['link']
    new_description = request.POST['description']
    document_type = request.POST["document_type"]
    if document_type == "video":
        Stall_Owner_documents.objects.create(stall_id=stall_text ,document_type = "V", document_title=new_title, document_description=new_description, document_link=new_link)
    elif document_type == "new_document":
        Stall_Owner_documents.objects.create(stall_id=stall_text , document_type = "D", document_title=new_title, document_description=new_description, document_link=new_link)

    return HttpResponseRedirect(f"/arena/stall_add_documents/{company_name}/{stall_text}/")



def new_representative(request, company_name, stall_text):
    name = request.POST['name']
    email = request.POST['email']
    mobile = request.POST['mobile']
    designation = request.POST['designation']

    Stall_Sales_Representatives.objects.create(stall_id = stall_text, name=name, email=email, mobile=mobile, designation= designation)

    return HttpResponseRedirect(f"/arena/stall_add_sales_representative/{company_name}/{stall_text}/")


def update_representative(request, company_name, stall_text):
    name = request.POST['name']
    temp_id = request.POST['id']
    email = request.POST['email']
    mobile = request.POST['mobile']
    designation = request.POST['designation']
    print(name,email,mobile,designation)
    print(stall_text)
    temp_data = Stall_Sales_Representatives.objects.get(stall_id = stall_text, id = temp_id)
    print("Temp Data is ",temp_data)
    temp_data.name = name
    temp_data.email = email
    temp_data.mobile = mobile
    temp_data.designation = designation
    temp_data.save()

    return HttpResponseRedirect(f"/arena/stall_add_sales_representative/{company_name}/{stall_text}/")
def schedule_call_by_user(request,company_name,stall_text):
    """
        get from user
        username
        email
        start date
        start time
    """    
    print("this is my data",request.POST)
    user_id = request.user.id
    print("this is user id",user_id)
    schedule_call = request.POST["schedule_call"]
    start_time,start_date = schedule_call.split(" ")
    users = MyUser.objects.get(id = MyUser.objects.get(id=request.user.id).id)
    name,email,mobile=users.name,users.email,users.mobile
    call_schedules.objects.create(
                                    stall_id = stall_text,
                                    mobile = mobile,
                                    name=name,
                                    email=email,
                                    selected_date="-".join(start_date.split('/')[::-1]),
                                    selected_time=start_time
                                    )
    return HttpResponseRedirect(
        reverse('main_website:stall_details', kwargs={'company_name': company_name, 'stall_text': stall_text}))
    # return render(requests, 'new/stall_details_page.html', context)

