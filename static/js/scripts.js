




$(document).ready(function () {
    var cart_visible;
    var cart_items_length=$(".cart-items-list").children('li').length;
    if(cart_items_length==0)
    {
        cart_visible="hidden"
    }
    else {
        cart_visible='visible'
    }
    var form=$('#form_add_to_cart');
    $("#phone_input").mask("375(99)999-99-99");
    $(document).mouseup(function (e) {
        var container=$(".cart-items");
        if(container.has(e.target).length===0){
            container.css("visibility","hidden");
        }


    });
    function basket_updating(data)
    {
           cart_visible="visible";
                product_id_cart_selector="#cart-item-"+data.product_id;
                    $('#cart_count').text('(' +data.cart_count+ ')');
                    if($('li').is(product_id_cart_selector))
                    {
                        var product_cart_info=$(product_id_cart_selector).children('.cart-item-container').children('.cart-item-row').children('.cart-item-info');
                       product_cart_info.children('.product-count-p').children('.product_count').text(data.count);
                        product_cart_info.children('.product_price').text(data.price);
                    }
                    else {
                     $('.cart-items ul').append('<li id=cart-item-'+data.product_id+' class="cart-item">' +
                         '<div class="container cart-item-container">' +
                            '<div class="row cart-item-row">' +
                            ' <div class="col-sm-3 cart-item-image">\n' +
                                 '<img class="cart-item-image" src='+data.image +' alt="">\n' +
                                '</div>' +
                         '<div class="col-sm-8 cart-item-info">' +
                         '<h5>' + data.name+'</h5>' +
                         '<p class="product-count-p"><span class="product_count">'+data.count+'</span> things </p>' +
                                     'price:<span class="product_price">'+ data.price+'</span> USD ' +
                         '</div>'+
                        '<a class="delete-item" href="/remove_from_cart/" data-product_id='+data.product_id+' >X</a>' +
                            '</div>' +
                         '</div>' +
                         '</li>'
           )}

    }
    form.on("submit",function (e) {
        e.preventDefault();
        var count = $('#count').val();
        var submit_btn=$('#submit_btn');
        var product_id=submit_btn.data("product_id");
        var product_name=submit_btn.data("product_name");
        var product_price=submit_btn.data("product_price")*count;

        var data={};
        var url=form.attr('action');
        var csrftoken=$("[name=csrfmiddlewaretoken]").val();
        data["csrfmiddlewaretoken"]=csrftoken;
        data["product_id"]=product_id;
        data["product_count"]=count;
        $.ajax({
                url:url,

            type:'POST',
            data:data,
            cache:true,
            success:function (data) {
                   basket_updating(data) ;
            },
            error:function () {console.log('error')

            }
            }
    );

    });

    $(".product-card-form").submit(function (e) {
        e.preventDefault();
         var btn_id=$(document.activeElement).attr('id');
         var btn=$('#' + btn_id );
          var data={};
        var url=$(".product-card-form").attr('action');
        var csrftoken=$("[name=csrfmiddlewaretoken]").val();
        data["csrfmiddlewaretoken"]=csrftoken;
        data["product_id"]=btn.data("product_id");
        data["product_count"]=btn.data("product_count");
         $.ajax({
                url:url,
            type:'POST',
            data:data,
            cache:true,
            success:function (data) {

                    basket_updating(data) ;
            },
            error:function () {console.log('error')

            }
            }
    );
    });


    $('.cart_open').on('click',function (e)
    {
        e.preventDefault();
        if(cart_visible==='visible')
        {
        $(".cart-items").css("visibility","visible");
        }
    });



    $('#search_field').on('input',function () {
        var search_form=$('#form-search-product');
        text=$("#search_field").val();
        console.log('change');
            $.ajax({
                 url:"/dynamic_search",
                type:"GET",
                data:{"search_text":text},
                success: function (data) {
                    console.log(data);
                    $("#search_results").empty();
                    $.each(data,function(key,value){

                    $("#search_results").append(

                        '<li style="{list-style-type: none;}">' +
                        '<a href=/product/'+key +'>' +
                        '<div class="container-fluid">'+
                        '<div class="row" style="border:1px solid rgb(200,200,200);">'+
                        '<div class="col-sm-4" style="display: inline-block; ">' +
                        '<img style="height:100px;" src="'+ value.product_image_url+'" alt="product image">' +
                        '</div>'+
                        '<div class="col-sm-8" style="max-width: 100%;max-height:100%;display: inline-block;">'+ '' +
                        '<h5>'+value.name+ ' </h5>'+'<p>Rate:' + value.rate+ '</p>' +value.price+' USD' +
                        '</div></div>' +
                        '</div>' +
                        '</a></li>')});
                },
                error(){console.log("error")}

            });
    });
    $(document).on('click',
        '.delete-item',function (e) {
        e.preventDefault();
        product_id = $(this).data("product_id");
        this_element=$(this).closest('li');
        var data={};
        data["product_id"]=product_id;
        url=$(this).attr('href');
        $.ajax({
                url:url,
            type:'POST',
            data:data,
            cache:true,
            success:function (data) {
                    if(data.cart_count=='0')
                    {
                        $('#cart_count').text('');
                         cart_visible="hidden";
                    }
                    else{
                    $('#cart_count').text('(' +data.cart_count+ ')');}
                this_element.remove();
            },
            error:function () {
                    console.log('error')

            }
            }
    );


        })
})