let list = document.querySelectorAll('.list .item');
let arr = [];
list.forEach(item => {
    item.addEventListener('click', function(event){
        // console.log(event.target.classList.contains('add'));
        if(event.target.classList.contains('add')){

            var itemNew = item.cloneNode(true);
            let checkIsset  = false;

            let listCart = document.querySelectorAll('.cart .item');
            
            listCart.forEach(cart =>{
               
                
                if(cart.getAttribute('data-key') == itemNew.getAttribute('data-key')){
                    checkIsset = true;
                   itemNew.remove();
                    // console.log(cart);
                    // cart.classList.add('danger');
                    // setTimeout(function(){
                    //     cart.classList.remove('danger');
                    // },1000)
                }
            })
            if(checkIsset == false){
                document.querySelector('.listCart').appendChild(itemNew);
                let sum = document.querySelector('.sum');
                let priceTotal = Number(itemNew.childNodes[3].childNodes[5].textContent.slice(1,))     //*!tuzatish kere*//
                let inpVal = Number(itemNew.childNodes[3].childNodes[7].value)
                let div = document.createElement('div');
                div.classList.add('one-product-price');

                // inpVal = inpVal * priceTotal;
                let val = inpVal * priceTotal;

                console.log(inpVal);
                
                if(inpVal > 1 && inpVal < 10){div.textContent ="0"+ inpVal + "/" + val;}
                if(inpVal > 1 && inpVal >= 10){div.textContent = inpVal + "/" + val;}

                itemNew.childNodes[3].childNodes[5].appendChild(div)
                let summauchun = Number(sum.textContent);

                summauchun += val;
                sum.textContent = summauchun;

                const url = 'http://127.0.0.1:8000/products/card/add/'
                var options = {
                    method: 'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    mode: 'same-origin'
                }
                var formData = new FormData();
                formData.append("product_id", itemNew.getAttribute('data-key'));
                formData.append("product_count", item.querySelector('.count').value);

                options.body = formData;

                fetch(url, options)
                .then((response) => response.json())
                .then((data) => {
                    if (data["status"] === "ok") {
        
                    }
                })
                .catch((error) => {
                    // Handle any errors that might occur during the fetch request
                    console.error("Error:", error);
                });
                 

            }
           
             

        }
    })
})
function Remove(key){
    let listCart = document.querySelectorAll('.cart .item');
    listCart.forEach(item => {
        if(item.getAttribute('data-key') == key){


            const url = 'http://127.0.0.1:8000/products/card/remove/'
            var options = {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin'
            }
            var formData = new FormData();
            formData.append("product_id", item.getAttribute('data-key'));

            options.body = formData;

            fetch(url, options)
            .then((response) => response.json())
            .then((data) => {
                if (data["status"] === "ok") {
                }
            })
            .catch((error) => {
                // Handle any errors that might occur during the fetch request
                console.error("Error:", error);
            });
            // let price = parseInt(item.querySelector('.price').textContent);
            // let parentItem = item.parentNode;

            // // Update the total sum
            // let sumElement = parentItem.querySelector('.sum');
            // let currentSum = parseInt(sumElement.textContent);
            // currentSum -= price;
            // sumElement.textContent = currentSum;
            item.remove();
            return;
        }
        else {
           
        }
    })
}


let sum = document.querySelector('.sum');

let cartClick = document.querySelector('.listCart');
cartClick.addEventListener('click', (e) => {
    // console.log(e.target.parentElement.previousElementSibling.previousElementSibling.previousElementSibling.textContent.slice(6,));
    // console.log(e.target.parentElement.previousElementSibling.previousElementSibling.previousElementSibling.childNodes[1].textContent.slice(0,2));
    if(e.target.tagName === 'I'){    /!*!remove*/
        let clickPrice = Number(e.target.parentElement.previousElementSibling.previousElementSibling.previousElementSibling.childNodes[1].textContent.slice(3,));
        console.log(e.target.parentElement.previousElementSibling.previousElementSibling.previousElementSibling.childNodes[1])
        let minuse = Number(sum.textContent);
        minuse = minuse - clickPrice ;
        sum.textContent = minuse;
    }

   if (e.target.tagName == "INPUT") {
    // console.log(e.target.parentElement.previousElementSibling.nextElementSibling.childNodes[5].childNodes[0].textContent.slice(1,));
    // let y = document.querySelector('.price')
    // console.log(y)
    let l = e.target.value
    if(e.target.value < 10 ) {
        l = '0' +  e.target.value
    }
        if(l < e.target.parentElement.previousElementSibling.nextElementSibling.childNodes[5].childNodes[1].textContent.slice(0,2))
        {
            console.log(e.target.parentElement.previousElementSibling.childNodes[1].textContent.slice(0,2))
            let n = Number(e.target.value);
            let m = Number(e.target.parentElement.previousElementSibling.nextElementSibling.childNodes[5].childNodes[1].textContent.slice(0,2));
            let s = Number(e.target.parentElement.previousElementSibling.nextElementSibling.childNodes[5].childNodes[0].textContent.slice(1,));
            let y = e.target.parentElement.previousElementSibling.nextElementSibling.childNodes[5].childNodes[1]
            let a = m - n;
            console.log(y.textContent.slice(3,))
            a = a * s
            let v = Number(y.textContent.slice(3,))
            y.textContent =`0${n}/${v - a}`; 
            // let shot = v - a;
            let nm = Number(sum.textContent);
            nm = nm - a;
            sum.textContent = nm;
            

            console.log(y)






        }
    }
});
// !comeeeeeeeeeennnnnnt
let title = document.querySelector('.center-title')
let menuss = document.querySelector('.previuse-ul')
let center = document.querySelectorAll('.list');


menuss.addEventListener('click', (e) => {
    if (e.target.tagName == 'LI'){
        // console.log(e.target.textContent);
        title.textContent = e.target.textContent
        // console.log(center)
        center.forEach((item) => {
            item.style.display="none";
            // console.log(item.className.includes(e.target.textContent))
            // console.log(item.className, e.target.textContent )
         if(item.className.includes(e.target.textContent)){
                item.style.display="grid";
        console.log(e.target.textContent);

        console.log(center)

            }
        })
    }  

})


// let cartList = document.querySelector('.listCart')

// // console.log(cartList.childElement)


// const le =  setInterval(() => {
//     console.log(cartList.childNodes)
// }, 1000);



// listCart.forEach((item) => {
//     console.log(item)
// })



