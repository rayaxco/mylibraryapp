console.log('js read')
var regForm=document.getElementById('registerForm');
if(regForm){
    regForm.addEventListener('submit',async function(event){
        event.preventDefault();

        const form=event.target;
        const formData=new FormData(form);
        const data=Object.fromEntries(formData.entries());

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
