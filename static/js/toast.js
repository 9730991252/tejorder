 let tostBox = document.getElementById('tostBox')
 function show_tost(msg, type) {
   let toast = document.createElement('div');
   toast.classList.add('tost');
   toast.innerHTML = `<i class="fa fa-check-circle" aria-hidden="true"></i> ${msg}`;
   
   if(type == 'error'){
     toast.classList.add('error');
     toast.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> ${msg}`;
    }
    if(type == 'Invalid'){
      toast.classList.add('invalid');
      toast.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> ${msg}`;
    }
    tostBox.appendChild(toast);
   setTimeout(function(){
     toast.remove()
   }, 1000)
 }