$(function() {
    $("#various1").fancybox({

    });
    $("#various2").fancybox({

    });
    $("#various3").fancybox({

    });


    if($.trim($('#edit-params').val())!=""){
        e_params = $.evalJSON($('#edit-params').val());
    }
    $('#add_param_btn_e').click(
        function () {
            e_params = $.evalJSON($('#edit-params').val());
            var name = $('#add_name_e').val();
            var must = $('#add_must_e').prop('checked');
            var type = $('#add_type_e').val();
            var t_default = $('#add_default_e').val();
            var description = $('#add_description_e').val();
            if ($.trim(name) == "" || $.trim(type) == "" || $.trim(description) == "") {
                alert("参数不合法！");
            }
            else {
                e_params.push({'name': name, 'must': must, 'type': type, 'default': t_default, 'description': description});
                $('#edit-params').val($.toJSON(e_params));
                //清空变量
                $('#add_name_e').val('');
                $('#add_type_e').val('');
                $('#add_default_e').val('');
                $('#add_description_e').val('');
            }
        }
    );


    c_params = new Array();
    $('#add_param_btn').click(
        function () {
            var name = $('#add_name').val();
            var must = $('#add_must').prop('checked');
            var type = $('#add_type').val();
            var t_default = $('#add_default').val();
            var description = $('#add_description').val();
            if ($.trim(name) == "" || $.trim(type) == "" || $.trim(description) == "") {
                alert("参数不合法！");
            }
            else {
                c_params.push({'name': name, 'must': must, 'type': type, 'default': t_default, 'description': description});
                //写入页面
                var tmp = '<tr><td>' + name + '</td>';
                tmp = tmp + '<td>' + must + '</td>';
                tmp = tmp + '<td>' + type + '</td>';
                tmp = tmp + '<td>' + t_default + '</td>';
                tmp = tmp + '<td>' + description + '</td>';
                $('#add_tmp_params').append(tmp);
                //清空变量
                $('#add_name').val('');
                $('#add_type').val('');
                $('#add_default').val('');
                $('#add_description').val('');
            }
        }
    );

    p_del = function(api_id){
        $('#pre-del').html(api_id);
    }

    $('#del-btn').click(function(){
        var api_id = $('#pre-del').text();
        $.ajax({
            url: '/admin/delete',
            data: {'api_id': api_id},
            type: 'POST',
            success: function(data){
                if(data=="ok"){
                    window.location.href="/admin";
                }
            },
            error: function(err){
                console.log(err);
            }
        })
    });
});

var preview_json = function () {

    try {
        //var api_return = eval('(' + $('#edit-result-1').val() + ')');
        var api_return = $.evalJSON($.trim($('#edit-result-1').val()));
        $('.api-result-1').css('display', 'block');
        $('.api-result-1').html('');
        $(renderjson.set_show_to_level('all')(api_return).innerHTML).appendTo($('.api-result-1'));
        //JSONFormatter.format(api_return, {'appendTo': '.api-result-1', 'list_id': 'json-1'});
    }
    catch (e) {
        alert('json格式不正确');
    }
}

var preview_json_1 = function () {
    try {
        var api_return = eval('(' + $('#hidden-api-result-2').val() + ')');
        $('.api-result-2').css('display', 'block');
        $('.api-result-2').html('');
        $(renderjson.set_show_to_level('all')(api_return).innerHTML).appendTo($('.api-result-2'));
        //JSONFormatter.format(api_return, {'appendTo': '.api-result-2', 'list_id': 'json-1'});
    }
    catch (e) {
        alert('json格式不正确');
    }
}

//新增接口
    add_api = function() {
        var format = new Array();
        var method = new Array();
        if ($('#json').prop('checked')) {
            format.push('JSON');
        }
        if ($('#xml').prop('checked')) {
            format.push('XML');
        }

        if ($('#get').prop('checked')) {
            method.push('GET');
        }
        if ($('#post').prop('checked')) {
            method.push('POST');
        }

        if ($.trim($('#add-name-l').val()) == "" || $.trim($('#add-description-l').val()) == "" ||
            $.trim($.toJSON(c_params)) == "" ) {
            alert("参数不合法！");
        }
        else {
            $.post('/admin/add', {
                'name': $('#add-name-l').val(),
                'description': $('#add-description-l').val(),
                'category': $('#add-category-l').val(),
                'format': format.join(','),
                'method': method.join(','),
                'auth': $('#add-auth-l').prop('checked'),
                'params': $.toJSON(c_params),
                'return': $('#hidden-api-result-2').val(),
                'notice': $('#add-notice-l').val()
            }, function (data) {
                if (data == "ok") {
                    window.location.href = "/admin";
                }
                else {
                    alert('未知异常');
                }
            })
        }
    }

edit_api = function(api_id) {
        var format = new Array();
        var method = new Array();
        if ($('#json-e').prop('checked')) {
            format.push('JSON');
        }
        if ($('#xml-e').prop('checked')) {
            format.push('XML');
        }

        if ($('#get-e').prop('checked')) {
            method.push('GET');
        }
        if ($('#post-e').prop('checked')) {
            method.push('POST');
        }

        if ($.trim($('#edit-description').val()) == "" || $.trim($('#edit-params').val()) == "") {
            alert("参数不合法！");
        }
        else {
            $.post('/admin/edit/' + api_id, {
                'description': $('#edit-description').val(),
                'category': $('#edit-category').val(),
                'format': format.join(','),
                'method': method.join(','),
                'auth': $('#edit-auth').prop('checked'),
                'params': $('#edit-params').val(),
                'return': $('#edit-result-1').val(),
                'notice': $('#edit-notice').val(),
                'changelog': $.trim($('#edit-changelog').val()),
                'test': $('#edit-test').val()
            }, function (data) {
                if (data == "ok") {
                    window.location.href = "/admin";
                }
                else {
                    alert('未知异常');
                }
            })
        }
    }