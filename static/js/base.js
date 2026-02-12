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
            console.log('login response ok')
            const data=await response.json();
            deleteAllCookies();
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

var adminButton=document.getElementById('admin-action');
if(adminButton){
    adminButton.addEventListener('click', async function(event){
        event.preventDefault();

        console.log('admin action button pressed')
        console.log('redirecting to admin actions'); // Clear the form
        window.location.href='/lib/admin-actions';

    });
}

var adminButton=document.getElementById('admin-action');
if(adminButton){
    adminButton.addEventListener('click', async function(event){
        event.preventDefault();
        console.log('admin action button pressed')

        try {
                    console.log('redirecting to admin actions'); // Clear the form
                    window.location.href='/lib/admin-actions';
                }
        catch(error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
        }
    });
}

var addBookForm=document.getElementById('addBookForm');
if(addBookForm){
    addBookForm.addEventListener('submit',async function(event){
        event.preventDefault();

        const form=event.target;
        const formData=new FormData(form);

    try{
        ('Trying..')
        //const response=await fetch('/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
        const response=await fetch('/lib/add-book',{method:'POST',body:formData});
        if(response.ok){
            window.location.href='/lib/admin-actions';
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

var logoutButton=document.getElementById('logoutButton');
if(logoutButton){
    logoutButton.addEventListener('click', async function(event){
        console.log('Logout button pressed');
        logout();
    });
}

var deleteBookButtons=document.getElementsByClassName('deleteBookButtons');
if(deleteBookButtons){
   for(let i=0;i<deleteBookButtons.length;i++){
        deleteBookButtons[i].addEventListener('click', async function(event){
            event.preventDefault();
            if(!confirm('Are you sure you want to delete this book?')){
                return;
            }
            else{
                token=getCookie('access_token');
                //initiate delete request
                const response= await fetch(
                `/lib/delete-book/${deleteBookButtons[i].value}`,
                {
                    method:'DELETE',
                    headers:{
                        'Authorization':`Bearer${token}`
                    }

                }
                );
                if(response.ok){
                    window.location.href='/lib/show-books'
                }
            }
        });
    }
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
        window.location.href = '/auth/login';
}

function deleteAllCookies(){
    const cookies = document.cookie.split(";");

        // Iterate through all cookies and delete each one
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1  ?  cookie.substr(0, eqPos) : cookie;
            // Set the cookie's expiry date to a past date to delete it
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
        }

}

function getCookie(name){
    if(document.cookie && document.cookie !==''){
        cookies=document.cookie.split(';')
        for(let i=0;i<cookies.length;i++){
            cookies[i]=cookies[i].trim();
            nameAndValue=cookies[i].split('=');
            if(name===nameAndValue[0]){
                //console.log(nameAndValue[1]);
                return nameAndValue[1]
            }
        }
    }
}