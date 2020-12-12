  // var username = 'shubham'
var roomName = null;
var chatSocket = null;
var username = null;
var reciever_id = null;
var NotificationSocket = null;
var main = null;
var connection_protocol = 'ws://'
if(window.location.href.replace('http://','').length == window.location.href.length){
  connection_protocol = 'wss://'
}

function showNotification() {
    console.log("I am inside this one")
    const notification = new Notification("New message incoming", {
    body: "You have some Message"
     })
}

function notifyMe() {
    console.log("I am inside notification")
    if (!window.Notification) {
        console.log('Browser does not support notifications.');
    } else {
        if (Notification.permission === 'granted') {
            showNotification();
        } else {
            Notification.requestPermission().then(function (p) {
                if (p === 'granted') {
                    showNotification();
                    console.log("allowed")
                } else {
                    console.log('User blocked notifications.');
                }
            }).catch(function (err) {
                console.error(err);
            });
        }
    }

}

NotificationSocket = new ReconnectingWebSocket(
    connection_protocol
    + window.location.host
    + '/ws/notifications/'
);
NotificationSocket.onopen = function(e){
  console.log('connected')
}

NotificationSocket.onmessage = function(e){
  console.log('notification recieved')

  user_id = JSON.parse(e['data'])['message']
  cloned_person = $('#user_id_'+user_id).clone();
  // // make it visible
  cloned_person.find('span').css('opacity',1);
  cloned_person.find('span').text(parseInt(cloned_person.find('span').text()) + 1);

  $('#user_id_'+user_id).remove();
  $("#friends>div:nth-child(1)").after(cloned_person);

  var x = document.getElementById("myAudio");
  x.play(); 
  $('#attendee_popup').css('color','red');

  // notifyMe()
}  

NotificationSocket.onclose = function(e) {
    console.log('notification closed');
    
};


function connect_chat(id,name,main_active = null){

      var childOffset = $(this).offset();
      var parentOffset = $(this).parent().parent().offset();
      var childTop = childOffset.top - parentOffset.top;
      var clone = $(this).find('img').eq(0).clone();
      var top = childTop+12+"px";
      
      $(clone).css({'top': top}).addClass("floatingImg").appendTo("#chatbox");                  
      
      setTimeout(function(){$("#profile p").addClass("animate");$("#profile").addClass("animate");}, 100);
      setTimeout(function(){
        $("#chat-messages").addClass("animate");
        $('.cx, .cy').addClass('s1');
        setTimeout(function(){$('.cx, .cy').addClass('s2');}, 100);
        setTimeout(function(){$('.cx, .cy').addClass('s3');}, 200);     
      }, 150);                            
      
      $('.floatingImg').animate({
        'width': "68px",
        'left':'108px',
        'top':'20px'
      }, 200);

      // var name = $(this).find("p strong").html();
      // var email = $(this).find("p span").html();                            

      $("#profile p").html(name);
      // $("#profile span").html(email);     
      
      $(".message").not(".right").find("img").attr("src", $(clone).attr("src"));                  
      $('#friendslist').fadeOut();
      $('#chatview').fadeIn();
    
      
      $('#close').unbind("click").click(function(){ 
        $('#chatview').fadeOut();
        $('#friendslist').fadeIn();
        chatSocket.close();
      });


    if (main_active !=null){
      main = 1;
    }  
    else{
      main = null;
    }

    try {
      chatSocket.close();
      if (main !=null){
        $('#chat-messages-main > div').remove();
      }
      else{
        $('#chat-messages > div').remove();
      }
    }
    catch{
      console.error('Chat Socket is not websocket'); 
    }

    reciever_id = id.split('_')[2];
    sender_id = $('.current_user').first().attr('id');
    roomName = reciever_id + '_' + sender_id;
    if(reciever_id < sender_id){
      roomName = reciever_id + '_' + sender_id + '_';    
    }
    else{
      roomName = sender_id  + '_' + reciever_id + '_';        
    }  

    chatSocket = new ReconnectingWebSocket(
        connection_protocol
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );




    chatSocket.onopen = function(e) {
      user_id = $('.current_user').first().attr('id');
      if(reciever_id == null){
        fetchMessages();
      }
      else{
        fetchMessages(reciever_id);
      }
    }

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        if (data['command'] === 'messages') {
          for (let i=0; i<data['messages'].length; i++) {
            createMessage(data['messages'][i]);
          }
        } else if (data['command'] === 'new_message'){
          createMessage(data['message']);
        }
        if (main !=null){
        $("#chat-messages-main").animate({ scrollTop: $('#chat-messages-main').prop("scrollHeight")}, 2000);          
        }
        else{
          $("#chat-messages").animate({ scrollTop: $('#chat-messages').prop("scrollHeight")}, 2000);
        }
        debugger;
    };

    chatSocket.onclose = function(e) {
      // debugger;
        console.log('Chat socket closed unexpectedly');
        
    };

    if (main != null){
      document.querySelector('#chat-message-input-main').onkeyup = function(e) {
          if (e.keyCode === 13) {  // enter, return

              document.querySelector('#send_main').click();
          }
      };
    }
    else{
      document.querySelector('#chat-message-input').onkeyup = function(e) {
          if (e.keyCode === 13) {  // enter, return
              document.querySelector('#send').click();
          }
      };      
    }

    username = $('.current_user').first().attr('name');

    document.querySelector('#send').onclick = function(e) {
        var messageInputDom = document.getElementById('chat-message-input');
        var message = messageInputDom.value;
        if (message.length != 0) {
          chatSocket.send(JSON.stringify({
              'command': 'new_message',
              'message': message,
              'from': username
          }));

          messageInputDom.value = '';
        }
    };

    try { 
        document.querySelector('#send_main').onclick = function(e) {
            var messageInputDom = document.getElementById('chat-message-input-main');
            var message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'command': 'new_message',
                'message': message,
                'from': username
            }));

            messageInputDom.value = '';
        };    
    }
    catch (e){
      console.log('wow');
    }

}







function fetchMessages(_reciever_id = null) {
  // debugger;
  if(_reciever_id == null){
    chatSocket.send(JSON.stringify({'command': 'fetch_messages','reciever_id':_reciever_id}));
  }
  else{
    chatSocket.send(JSON.stringify({'command': 'fetch_messages','reciever_id':_reciever_id}));    
  }
}

function createMessage(data) {
  
  var author = data['author'];

  var message_div = document.createElement('div');
  var bubble_div = document.createElement('div');
  bubble_div.className = 'bubble'

  bubble_div.textContent = data['content'];
  
  if (author === username) {
    message_div.className = 'message';
  } else {
    message_div.className = 'message right';     
  }
  message_div.appendChild(bubble_div);
  if (main !=null){
    document.querySelector('#chat-messages-main').appendChild(message_div);    
  }
  else{
    document.querySelector('#chat-messages').appendChild(message_div);
  }
  
}