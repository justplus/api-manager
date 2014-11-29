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
});
