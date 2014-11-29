$(function(){
    $('#search-btn').click(function(){
        $.ajax({
            url: '/search',
            data: {'keyword': $.trim($('#search-kw').val())},
            type: 'POST',
            success:function(data){
                $('#search-result').html(data);
            },
            error:function(err){
                console.log(err);
            }
        });
    });

    $("#search-kw").keydown(function(e){
        var curKey = e.which;
        if(curKey == 13){
            $("#search-btn").click();
            return false;
        }
    });

    $("#password").keydown(function(e){
        var curKey = e.which;
        if(curKey == 13){
            $("#login-btn").click();
            return false;
        }
    });

    $("#login-btn").click(function(){
        if($.trim($('#name').val())=="" || $.trim($('#password').val())==""){
            alert("用户名或密码不能为空！");
        }
        else{
            $.ajax({
                url: '/login',
                data: {'user_name': $.trim($('#name').val()), 'password': $.trim($('#password').val())},
                type: 'POST',
                success:function(data){
                    if(data == 'ok'){
                        window.location.href = '/admin';
                    }
                    else{
                        alert('用户名或者密码错误！');
                    }
                },
                error:function(err){
                    console.log(err);
                }
            });
        }
    });
});
