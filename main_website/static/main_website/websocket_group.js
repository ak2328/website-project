var roomgroupName = null;
var chatgroupSocket = null;
var username = null;
var reciever_id = null;
// var NotificationgroupSocket = null;

function connect_chat_group(id,main_active = null){

      connection_protocol = 'ws://'
      if(window.location.href.replace('http://','').length == window.location.href.length){
        connection_protocol = 'wss://'
      }

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
      debugger;
      // var name = $(this).find("p strong").html();
      // var email = $(this).find("p span").html();                            
      $("#profile p").html('Group Chat');
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

    chatSocket = new ReconnectingWebSocket(
        connection_protocol
        + window.location.host
        + '/ws/'
        + 'groupchat'
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
        }

        messageInputDom.value = '';
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