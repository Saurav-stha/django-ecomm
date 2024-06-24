var updateBtns = document.getElementsByClassName('update-cart')

for (var i=0; i < updateBtns.length; i++){

    updateBtns[i].addEventListener('click', function(){

        var productId = this.dataset.product
        var action = this.dataset.action
        var productName = this.dataset.prodname
    
        console.log("id: ",productId, '  action: ',action, ' name: ', productName)

        console.log("user:  ", user)
        
        if ( user === "AnonymousUser"){
            console.log("i have never met this man in my life")
        }
        else{
            // console.log("eii what up",user)
            updateUserOrder(productId, action)
            
        }

    })

}

function updateUserOrder(productId, action){
    console.log("user logged in. sending data...")

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data)=>{
        // no reload update of cart qty in index
        updateCartTotal();
        updateCartItem(productId, action);

        console.log('dataa: ',data)
    })
}
