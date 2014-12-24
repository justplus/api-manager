/**
 * Created by justplus on 2014/12/14.
 */
var menu_selected_item;
$(function(){
    $('#menu-api-list').hover(function(){
        $('#submenu').fadeIn(500);
    }, function(){});

    $('#menu-expand').hover(function(){},function(){
        $('#submenu').fadeOut(500);
    })

    $('.submenu-a').click(function(){
        $('#submenu').css("display", "none");
    });

    var a=$(".top-nav-menu li a");
    //menu_selected_item = 0;

    /*li.click(function(){
          $(this).addClass("selected").siblings().removeClass("selected");
    });*/



    if(window.location.href.indexOf('/introduction') > 0){
        menu_selected_item = 0;
    }
    else if(window.location.href.indexOf('/guide') > 0){
        menu_selected_item = 1;
    }
    else if(window.location.href.indexOf('/changelog') > 0){
        menu_selected_item = 2;
    }
    else if(window.location.href.indexOf('/notification') > 0){
        menu_selected_item = 4;
    }
    else{
        menu_selected_item = 3;
    }

    $(".top-nav-menu").children().eq(menu_selected_item).addClass("selected").siblings().removeClass("selected");

    $('.top-login').hover(function(){
        $('#sublogin').fadeIn(500);
    }, function(){});

    $('.top-login').hover(function(){},function(){
        $('#sublogin').fadeOut(500);
    })

    $('.login-a').click(function(){
        $('#sublogin').css("display", "none");
    });

    $("#search-kw").keydown(function(e){
        var curKey = e.which;
        if(curKey == 13){
            if($.trim($('#search-kw').val())==''){
                window.location.href='/';
            }
            else{
                window.location.href='/search/' + $.trim($('#search-kw').val());
            }

            return false;
        }
    });

    solved = function(id){
        $.ajax({
            url: '/feedback',
            data: {
                'feed_type': -1,
                'id': id
            },
            type: 'POST',
            success:function(data){
                if(data == 'ok'){
                    window.location.href="/feedback";
                }
            },
            error:function(data){
                alert("未知异常");
            }
        });
    }
})