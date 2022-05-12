// console.log('working')
// const signup = document.querySelector('#sign-up-section')
// const signin = document.querySelector('#sign-in-section')
// document.querySelector('#signin-item').addEventListener('click',function(){
//     signup.style.display = "none"
//     signin.style.display = "block"
// })
// document.querySelector("#signup-item").addEventListener('click', function(){
//     signin.style.display = "none"
//     signup.style.display = "block"
// })

// document.querySelector("body").addEventListener('click', function(){
//     document.querySelector(".message_area").style.display = 'none'
// })
function show_password(){
    const toggle_show_passwd = document.querySelector('#togglePassword');
    const password = document.querySelector('#login_password');
    const type = password.getAttribute("type") === "password" ? "text" : "password";
    const inner = toggle_show_passwd.innerText === "Show" ? "Hide" : "Show";
    password.setAttribute('type', type);
    toggle_show_passwd.innerText = inner
    
    console.log(inner)
}
