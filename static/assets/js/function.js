console.log("working Fine");

const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"];

$("#commentForm").submit(function(e){

    e.preventDefault();
    let dt = new Date();
    let time= dt.getDate() + " "+ monthNames[dt.getUTCMonth()] +", " + dt.getFullYear();


    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response){
            console.log("comment saVED IN DB");


            if(response.bool == true){
                $("#review-response").html("Review added Successfully")
                $(".hide-comment-form").hide()

                let _html= '<div class="review-o u-s-m-b-15">'
                    _html +='<div class="review-o__info u-s-m-b-8">'

                    _html +='<span class="review-o__name">'+response.context.user +'</span>'

                    _html +='<span class="review-o__date">'+ time +'</span></div>'
                    for(let i=1; i<= response.context.rating; i++){

                        _html += '<i class="fas fa-star text: warnnig"></i>'
                    }

                    
        
                    _html +='<span>(4)</span></div>'

                    _html +='<p class="review-o__text">'+ response.context.review +'</p>'
                    _html +='</div>'

                $(".comment-list").prepend(_html)

            }

        }
    })

})

$(document).ready(function(){

    //Add to cart functionality

    $(".add-to-cart-btn").on("click", function(e){
        e.preventDefault();
        let this_val =$(this)
        let index = this_val.attr("data-index")
        let quantity = $(".product-quantity-" + index ).val()
        let product_title = $(".product-title-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text().trim()
    
        let product_image= $(".product-image-" + index).val()
        console.log("Quantity:", quantity);
        console.log("product_title:", product_title);
        console.log("PID:", product_id);
        console.log("product_image:", product_image);
        console.log("product_price:", product_price);
        console.log("this_val:", this_val);

        $.ajax({
            url: '/add-to-cart',
            data:{
                'id': product_id,
                'pid': product_id,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
                'image': product_image,
            },
            dataType: 'json',
            beforeSend: function(){
    
                console.log("Adding product to the cart...");
            },
    
            success:function(response){

    
                this_val.html("✓");
                console.log("Added product to the cart...");
                $(".cart-items.count").text(response.totalcartitems)
    
            },
        })


    })



    $(".delete-product").on("click", function(){
        let product_id= $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("productId: ", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: 'json',
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            },
        })

    })

    $(".update-product").on("click", function(){
        let product_id= $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-"+ product_id).val()
    
        console.log("productId: ", product_id);
        console.log("productqty: ", product_quantity);


        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty": product_quantity,
            },
            dataType: 'json',
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            },
        })

    })


    // Adding to wishlist

    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val= $(this)

        console.log("Product Id :", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data:{
                'id': product_id,
            },
            dataType: "json",
            beforeSend:function(){
                
                console.log("Adding to wishlist ....");
                
            },

            success:function(response){
                
                if(response.bool == true){
                    console.log("Added to wishlist ....");
                }

            }
        })

    })


})

