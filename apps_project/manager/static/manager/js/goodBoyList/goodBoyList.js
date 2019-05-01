(function () {
    'use strtic';

    // 初始名单展示
    function listShow(){
        $(".g-body-goodBoy-list tbody").html('<h3 style="width:400%;display:flex;color:#f0ad4e;justify-content:center;">数据刷新中，请稍后...</h3>');

        $.ajax({
            url: '/listShowJson/',
            type: 'POST',
            headers: {
                "X-CSRFToken": $.cookie('csrftoken')
            },
            success: function (data) {
                $(".g-body-goodBoy-list tbody").empty();
                for(var i=0;i<data.length;i++){
                    var listHtml =
                            `
                            <tr>
                                <td class="g-body-goodBoy-id">${data[i].id}</td>
                                <td>
                                    <input class="g-body-goodBoy-name" autocomplete="off" type="text" name='note' value='${data[i].name}'>
                                </td>
                                <td>
                                    <input class="g-body-goodBoy-note" autocomplete="off" type="text" name='note' value='${data[i].note}'>
                                </td>
                                <td>
                                    <input class="g-body-goodBoy-money" autocomplete="off" type="text" name='money' value='${data[i].money}'>
                                </td>
                                <td>
                                    <div index=${data.length - i} class="g-body-goodBoy-sub">修改</div>
                                    <div index=${data.length - i} class="g-body-goodBoy-del">删除</div>
                                    <div class="g-body-goodBoy-alert-meg"></div>
                                </td>
                            </tr>
                            `;
                    $(".g-body-goodBoy-list tbody").prepend(listHtml)
                }
                listAlter();
                listDel()
            },
        });
    }

    // 添加名单
    function listAdd(){
        $(".g-body-goodBoy-userSub").click(function(){
            var confirma = confirm('确认添加吗？');
            if(confirma){
                var nameSub = $("input")[0].value;
                var noteSub = $("input")[1].value;
                var moneySub = $("input")[2].value;

                moneySub = parseInt(moneySub * 100);

                if(nameSub != '' && moneySub != ''){
                    $(".g-body-goodBoy-list tbody").html('<h3 style="width:400%;display:flex;color:#f0ad4e;justify-content:center;">增加成功！数据刷新中，请稍后...</h3>');
                    $.ajax({
                        url: '/addGoodBoyMeg/',
                        type: 'POST',
                        headers: {
                            "X-CSRFToken": $.cookie('csrftoken')
                        },
                        data: {
                            'name':nameSub,
                            'note':noteSub,
                            'money':moneySub,
                        },
                        success: function(data) {
                            $('input').val('');
                            listShow()		// 重新加载数据
                        },
                        error:function(){
                            $(".g-body-goodBoy-userSub-meg").html('<div style="color:#c9302c">失败！</div>');
                        }
                    });
                }else{
                    alert('请完善需要的值！')
                }
            }
        });
    }

    // 修改名单
    function listAlter(){
        $('.g-body-goodBoy-sub').click(function(){
            var confirma = confirm('确认修改吗？');
            if(confirma) {
                var index = $(this).attr('index') - 1;
                var id = $('.g-body-goodBoy-id')[index].innerHTML;
                var name = $('.g-body-goodBoy-name')[index].value;
                var note = $('.g-body-goodBoy-note')[index].value;
                var money = $('.g-body-goodBoy-money')[index].value;

                if(name != '' && money != ''){
                    $.ajax({
                        url: '/alterGoodBoyMeg/',
                        type: 'POST',
                        headers: {
                            "X-CSRFToken": $.cookie('csrftoken')
                        },
                        data: {
                            'id': id,
                            'name': name,
                            'note': note,
                            'money': money
                        },
                        success: function (data) {
                            $('.g-body-goodBoy-alert-meg')[index].innerHTML = '<div style="color:#19b955">' + data + '！</div>';
                            setTimeout(function () {
                                $('.g-body-goodBoy-alert-meg')[index].innerHTML = '';
                            }, 10000);
                        },
                        error: function () {
                            $('.g-body-goodBoy-alert-meg')[index].innerHTML = '<div style="color:#c9302c">' + data + '！</div>';
                            setTimeout(function () {
                                $('.g-body-goodBoy-alert-meg')[index].innerHTML = '';
                            });
                        }
                    });
                }else{
                    alert('请完善需要的值！')
                }
            }
        });
    }

    // 删除名单
    function listDel(){
        $('.g-body-goodBoy-del').click(function(){
            var confirma = confirm('确认删除吗？');
            if(confirma) {
                var index = $(this).attr('index');
                index -= 1;
                var id = $('.g-body-goodBoy-id')[index].innerHTML;
                var name = $('.g-body-goodBoy-name')[index].value;

                $(".g-body-goodBoy-list tbody").html(`<h3 style="width:400%;display:flex;color:#f0ad4e;justify-content:center;">${name}删除成功！数据刷新中，请稍后...</h3>`);

                $.ajax({
                    url: '/delGoodBoyMeg/',
                    type: 'POST',
                    headers: {
                        "X-CSRFToken": $.cookie('csrftoken')
                    },
                    data: {
                        'id': id,
                    },
                    success: function () {
                        $(".g-body-goodBoy-list tbody").empty();
                        listShow()
                    },
                    error: function () {
                        $(".g-body-goodBoy-userSub-meg").html('<div style="color:#c9302c">失败！</div>');
                    }
                });
            }
        });
    }

	listShow();
	listAdd();
	listDel();
}());