const signup = document.querySelector('#sign-up-section')
const signin = document.querySelector('#sign-in-section')
document.querySelector('#signin-item').addEventListener('click',function(){
    signup.style.display = "none"
    signin.style.display = "block"
})
document.querySelector("#signup-item").addEventListener('click', function(){
    signin.style.display = "none"
    signup.style.display = "block"
})