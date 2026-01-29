console.log('js read')
var regForm=document.getElementById('registerForm');
if(regForm){
    regForm.addEventListener('submit',async function(event){
        event.preventDefault();

        const form=event.target;
        const formData=new FormData(form);
        const data=Object.fromEntries(formData.entries());

        if(data.password !== data.password2){
            alert('passwords do not match!')
            return
        }

        payload={
         username:data.username,
         email:data.email,
         first_name:data.firstname,
         last_name:data.lastname,
         role:data.role,
         password:data.password,
         is_active:true,
         phone_number:data.phone
        }
        console.log(payload);


    try{
        //const response=await fetch('/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
        const response=await fetch('/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
        if(response.ok){
            window.location.href='/auth/login';
        }
        else{
            const errordata=response.json();
            alert(`error:${errordata.message}`);
        }
    }
    catch(error){
        console.log('error:',error);
        alert('an error occurred, please try again');
    }
    });
}
var loginForm=document.getElementById('loginForm');
if(loginForm){
    loginForm.addEventListener('submit',async function(event){
        event.preventDefault();

        const form=event.target;
        const formData=new FormData(form);
        const data=Object.fromEntries(formData.entries());



        loginPayload={
         username:data.username,
         password:data.password
        }
        console.log(loginPayload);


    try{
        //const response=await fetch('/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
        const response=await fetch('/auth/token',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(loginPayload)});
        if(response.ok){
            const data=await response.json();
            logout();
            document.cookie=`access_token=${data.access_token}; path=/`;
//            console.log(data.access_token);
            window.location.href='/lib/home';
        }
        else{
            const errordata=response.json();
            alert(`error:${errordata.message}`);
        }
    }
    catch(error){
        console.log('error:',error);
        alert('an error occurred, please try again');
    }
    });
}

function logout(){
    const cookies = document.cookie.split(";");

        // Iterate through all cookies and delete each one
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1  ?  cookie.substr(0, eqPos) : cookie;
            // Set the cookie's expiry date to a past date to delete it
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
        }

        // Redirect to the login page
        window.location.href = '/auth/login-page';
}