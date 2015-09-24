$(function(){
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
                data: {'user_name': $.trim($('#name').val()), 'password': $.md5($.trim($('#password').val()))},
                type: 'POST',
                success:function(data){
                    if(data == 'wrong'){
                        alert('用户名或者密码错误！');
                    }
                    else if(data == 'admin'){
                        window.location.href = '/admin';
                    }
                    else{
                        window.location.href = '/';
                    }
                },
                error:function(err){
                    console.log(err);
                }
            });
        }
    });

    $("#register-btn").click(function(){
        var reg = /^[a-zA-Z]{2,15}[0-9]{0,2}$/;
        if($.trim($('#name').val())=="" || $.trim($('#password').val())==""){
            alert("用户名或密码不能为空！");
        }
        else if(!reg.test($.trim($('#name').val()))){
            alert("用户名不合法！");
        }
        else{
            $.ajax({
                url: '/register',
                data: {'user_name': $.trim($('#name').val()), 'password': $.md5($.trim($('#password').val()))},
                type: 'POST',
                success:function(data){
                    if(data == 'wrong'){
                        alert('注册失败，用户名可能重复');
                    }
                    else if(data == 'admin'){
                        window.location.href = '/admin';
                    }
                    else{
                        window.location.href = '/';
                    }
                },
                error:function(err){
                    console.log(err);
                }
            });
        }
    });

    follow = function($elem, user_id, api_id){
        $.ajax({
            url: '/follow',
            data: {'user_id': user_id, 'api_id': api_id},
            type: 'POST',
            success:function(data){
                if(data == 'wrong'){
                    alert('未知异常');
                }
                else if(data == 'login needed'){
                    window.location.href="/login";
                }
                else if(data == 'ok'){
                    //$elem.innerHTML='取消关注';
                    //$($elem).css('background', '#1cb841');
                    $($elem).attr('src', '../static/images/collect.png');
                    $($elem).attr('title', '取消关注');
                }
                else if(data == 'uok'){
                    //$elem.innerHTML='+ 关注';
                    //$($elem).css('background', '#1f4e7c');
                    $($elem).attr('src', '../static/images/uncollect.png');
                    $($elem).attr('title', '关注');
                }
            },
            error:function(err){
                console.log(err);
            }
        });
    };
});
