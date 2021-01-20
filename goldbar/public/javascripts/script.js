var check = function(list_no, name) {
    location.href = '/check?list_no='+list_no+'&name='+name;
    alert("맛점! "+name+" 가자~~");
}
   
var refresh = function() {
    location.href = '/';
}

var clean = function() {
    location.href = '/clean';
}

var add = function() {
    var name = document.getElementById('name').value;
    if(name != ''){
        location.href = '/add?name='+name;
    }else{
        alert('공백');
        //document.getElementById('alert-text').classList.add('show');
    }
}

var drop = function(list_no) {
 
if(confirm('삭제하시겠습니까?'))
   location.href = '/drop?list_no='+list_no;

}


