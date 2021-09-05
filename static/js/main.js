const btn_delete = document.querySelectorAll('.btn-delete');

if (btn_delete) {
    const btn_arr = Array.from(btn_delete);
    btn_arr.forEach((btn) => {
        btn.addEventListener('click', (e) => {    
            console.log(btn[0]);   
            if(!confirm('¿Are you sure you delete this user?')){
                e.preventDefault();
            }
        });      
    });
}
