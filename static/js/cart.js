var updateBtns = document.getElementsByClassName('update-cart')

for (var i=0; i < updateBtns.length; i++){

    updateBtns[i].addEventListener('click', function(event){

        var productId = this.dataset.product
        var action = this.dataset.action
        var productName = this.dataset.prodname
    
        console.log("id: ",productId, '  action: ',action, ' name: ', productName)

        console.log("user:  ", user)
        
        if ( user === "AnonymousUser"){
            addCookieItem(productId, action)
        }
        else{
            // console.log("eii what up",user)

            updateUserOrder(productId, action)
            
        }

    })

}


function addCookieItem(prodId, action){

    if (action == 'add'){

        if (cart[prodId] == undefined)
            cart[prodId] = {'quantity':1}
        else
            cart[prodId]['quantity'] += 1  
        
    }
    else if (action == 'remove'){
        cart[prodId]['quantity'] -= 1
        if (cart[prodId]['quantity'] <= 0 ){
            console.log("removed the item ")
            delete cart[prodId]
        }
    }
    updateCartTotal();
    updateCartItem(prodId, action);

    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    console.log('cart: ',cart)
    console.log("i have never met this man in my life")


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
