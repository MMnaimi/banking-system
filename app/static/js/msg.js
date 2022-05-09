document.querySelector("body").addEventListener('click', function(){
    document.querySelector(".message_area").style.display = 'none'
})

document.querySelector('#transfer').addEventListener('click', function(event){
    userconfirm = confirm("Are you sure to transfer?");
    if (userconfirm == false){
        event.preventDefault()
    }
})
document.querySelector('#delete-user').addEventListener('click', function(event){
    userconfirm = confirm("Are you sure to delete this user?");
    if (userconfirm == false){
        event.preventDefault()
    }
})