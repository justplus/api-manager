try{
    var api_return = eval('('+ $('#hidden-api-result').text() +')');
    /*if($.trim($('#hidden-api-result').text()).substr(0,1)!='{' && $.trim($('#hidden-api-result').text()).substr(0,1)!='['){
        $('.api-result').html($('#hidden-api-result').text());
    }
    else{
        JSONFormatter.format(api_return, {'appendTo' : '.api-result'});
    }*/
    $(renderjson.set_show_to_level('all')(api_return).innerHTML).appendTo($('.api-result'));
}
catch(e){
    $('.api-result').html($('#hidden-api-result').text());
}


$(function(){
    $("#doc-feed-back").fancybox({
        'scrolling' : 'no'
    });

    $("#api-feed-back").fancybox({
        'scrolling' : 'no'
    });

    $('#doc_feedback_btn').click(function(){
        if($.trim($('#feedback_content').val()) == ''){
            $('#err_msg').css('display', 'inline-block');
            return;
        }
        $.ajax({
            url: '/feedback',
            data: {'feed_type': 0, 'feed_content': $('#feedback_content').val() },
            type: 'POST',
            success:function(data){
                if(data == 'ok'){
                    $.fancybox.close();
                    alert('感谢您的反馈！');
                }
            },
            error:function(data){

            }
        });
    });

    $('#api_feedback_btn').click(function(){
        if($.trim($('#api_url').val())=='' || $.trim($('#feedback_content').val())==''){
            $('#err_msg').css('display', 'inline-block');
            return;
        }
        $.ajax({
            url: '/feedback',
            data: {
                'feed_type': 1,
                'api_id': $('#api_id').text(),
                'api_url': $('#api_url').val(),
                'feed_content': $('#feedback_content').val()
            },
            type: 'POST',
            success:function(data){
                if(data == 'ok'){
                    $.fancybox.close();
                    alert('感谢您的反馈，我们将及时解决并反馈');
                }
            },
            error:function(data){

            }
        });
    });

    url_full = false;
    $('#full-url').click(function(){
        if(url_full == false){
            $(this).text('简短URL');
            $('#test-param').val($('#test-param').val() + '&version=1.0&format=json&appkey=KtSNKxk3&access_token=changyanyun');
            $('#test-param').focus().select();
            url_full = true;
        }
        else{
            $(this).text('完整URL');
            $('#test-param').val($('#test-param').val().replace('&version=1.0&format=json&appkey=KtSNKxk3&access_token=changyanyun', ''));
            $('#test-param').focus();
            url_full = false;
        }

    });

    $('#api-request').click(function(){
        var method = $("#test-format").find("option:selected").text();
        $.ajax({
            url: '/test',
            data: {'method': method, 'url': $.trim($('#test-param').val())},
            type: 'POST',
            success:function(data){
                var data = $.evalJSON(data);
                if(data.status_code == '200'){
                    $('.test-result').css('background', 'rgba(186, 245, 171, 1)');
                    $('.test-result').html('');
                    if($.trim(data.content).substr(0,1)!='{' && $.trim(data.content).substr(0,1)!='['){
                        $('.test-result').html(data.content);
                    }
                    else{
                        //JSONFormatter.format(data.content, {'appendTo' : '.test-result', 'list_id': 'json-3'});
                        $(renderjson.set_show_to_level('all')(data.content).innerHTML).appendTo($('.test-result'));
                    }
                }
                else{
                    $('.test-result').css('background', 'rgba(255, 143, 143, 1)');
                    $('.test-result').html(data.content.subErrors[0].message);
                }
                //JSONFormatter.format(data.content, {'appendTo' : '#test_result'});
            },
            error: function(err){
                console.log(err);
            }
        });
        /*$.post('/test', {'method': method, 'url': $.trim($('#test-param').val())}, function(data){
            var data = $.toJSON(data);
            if(data.status_code == '200'){
                $('#test-result').css('background', 'rgba(186, 245, 171, 1)');
            }
            else{
                $('#test-result').css('background', 'rgba(255, 143, 143, 1)');
            }
            JSONFormatter.format(data.content, {'appendTo' : '.test_return'});
        })*/
    });

    $('#test-param').on('keypress', function(e){
        var code = (e.keyCode ? e.keyCode : e.which);
         if(code == 13) {
             e.preventDefault();
             $('#api-request').click();
         }
    });

    $(window).scroll(function(){
        if($(window).scrollTop()>100){
            $('#api-to-top').fadeIn(500);
        }
        else{
            $('#api-to-top').fadeOut(500);
        }
    });

    $('#api-to-top').click(function(){
        $('body,html').animate({scrollTop:0},400);
        return false;
    });
});
