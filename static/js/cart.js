

var updateBtns = document.getElementsByClassName('update-cart')

for (var i=0; updateBtns.length; i++){

    updateBtns[i].addEventListener('click', function(){

        var productId = this.dataset.product
        var action = this.dataset.action
    
        console.log("id: ",productId, '  action: ',action)

        console.log("user:  ", user)
        
        if ( user === "AnonymousUser")
            console.log("i have never met this man in my life")
        else
            console.log("eii what up",user)
    })

}
