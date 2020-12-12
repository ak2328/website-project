  // var username = 'shubham'
// var roomName = null;
// var analyticsSocket = null;
// var username = null;
// var reciever_id = null;
// var NotificationSocket = null;


const pageurl = window.location.href;
// var pagename = window.location.href.split('/')[-3]

// pageurl.split('/')
const url_details = window.location.href.replace('http://','').replace('https://','').replace('www.','').replace(window.location.host,'').split('/').slice(1,-1)
// pagename = 
var analyticsSocket = null
if(window.location.href.replace('http://','').length == window.location.href.length){
  analyticsSocket = new WebSocket(    
        'wss://'
        + window.location.host
        + '/ws/analytics/'

  );
}
else{
  analyticsSocket = new WebSocket(    
      'ws://'
      + window.location.host
      + '/ws/analytics/'    
  );
}

analyticsSocket.onopen = function(e) {
  analyticsSocket.send(JSON.stringify({'pagename': url_details[1],'company_name':url_details[2],'stall_url':url_details[3]}));
};

analyticsSocket.onmessage = function(e) {
    console.log('data saved');
};

analyticsSocket.onclose = function(e) {
    console.error('Chat socket closed');
};


function stall_pdf(){
	analyticsSocket.send(JSON.stringify({'pagename': 'stall_pdf','company_name':url_details[2],'stall_url':url_details[3]}));
	return true;
}


function stall_website(){
	analyticsSocket.send(JSON.stringify({'pagename': 'stall_website','company_name':url_details[2],'stall_url':url_details[3]}));
	return true;
}

function stall_whatsapp(){
  analyticsSocket.send(JSON.stringify({'pagename': 'stall_whatsapp','company_name':url_details[2],'stall_url':url_details[3]}));
  return true;
}

function stall_document(){
  analyticsSocket.send(JSON.stringify({'pagename': 'stall_document','company_name':url_details[2],'stall_url':url_details[3]}));
  return true;  
}
