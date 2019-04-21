(function(){
	'use strict';

	var Email = {
		Send:function(){
			$.ajax({
				// 获取邮件模板
				url: '/resources/manager/model/resetPwd.html',
				type: 'GET',
				success: function (data) {
					var myDate = new Date();
					var y = myDate.getFullYear(),
						m = myDate.getMonth() + 1,
						d = myDate.getDate(),
						H = myDate.getHours(),
						M = myDate.getMinutes();

					// 一波强行替换
					data = data.replace('MessyUser','Messy');
					data = data.replace('MessyOperation','登录管理台');
					data = data.replace('MessyID','1');
					data = data.replace('MessyTime',`${y}-${m}-${d} ${H}:${M}`);
					data = data.replace('MessyIP',returnCitySN["cip"]+','+returnCitySN["cname"]);
					data = data.replace('MessyA','https://www.messys.top/resetPwd');
					data = data.replace('MessyA','https://www.messys.top/resetPwd');

					// 调用发送邮件接口
					$.ajax({
						url: '/emailSend/',
						type: 'POST',
						headers: {
							"X-CSRFToken": $.cookie('csrftoken')
						},
						data:{
							'title':'Messy的邮件验证',
							'context':data,
							'toEmail':'messygao@qq.com',
						},
						success: function (data) {
							console.log(data);						// 打印成功信息
						}
					});
				}
			});
		},
	};
	var Menu = {
		main:function(){
			$('.g-framework-left-options-all').click(function(){
				$(this).find('.g-framework-left-options-list-open').toggleClass('g-framework-left-options-list-open-active');
				$(this).find('.g-framework-left-options-list').toggleClass('g-framework-left-options-list-active');
				$(this).find('.g-framework-left-options-options-block').slideToggle(500)
			})
		}
	};
	var Templates = {
		server:function(){
			$('.g-body').empty();
			window.location.href = ".";
		},
		serverOperation:function(){
			var template = $("<div>");
			template.load('/resources/manager/model/managerTemplates/serverOperation/serverOperation.html');
			$('.g-body').empty();
			$('.g-body').append(template);
			$('.g-body-loading').hide()
		},
		articlesImportMDApp:function(){
			var template = $("<div>");
			template.load('/resources/manager/model/managerTemplates/articlesImportMDApp/articlesImportMD.html');
			$('.g-body').empty();
			$('.g-body').append(template);
			$('.g-body-loading').hide()
		},
		articlesImportMDHtml:function(){
			var template = $("<div>");
			template.load('/resources/manager/model/managerTemplates/articlesImportMDHTML/articlesImportMD.html');
			$('.g-body').empty();
			$('.g-body').append(template);
			$('.g-body-loading').hide()
		},
		goodBoyList:function(){
			var template = $("<div>");
			template.load('/resources/manager/model/managerTemplates/goodBoyList/goodBoyList.html');
			$('.g-body').empty();
			$('.g-body').append(template);
			$('.g-body-loading').hide()
		},
	};
	var TempldatesShow = {
		main:function (){
			$('#j-server-1').click(function(){Templates.server()});
			$('#j-server-2').click(function(){Templates.serverOperation()});
			$('#j-articles-2').click(function(){Templates.articlesImportMDApp()});
			$('#j-articles-3').click(function(){Templates.articlesImportMDHtml()});
			$('#j-goodBoy-1').click(function(){Templates.goodBoyList()});
		}
	};

	window.onload = function(){
		// 上报功能暂时放弃（得买阿里云邮箱服务），改为数据库存储登录记录
		// var emailSendLife = $.cookie('emailSend');		// 邮件上报IP
		// if(emailSendLife != '1'){
		// 	Email.Send();								// ip邮件上报
		// 	$.cookie('emailSend','1',{expires:1});		// 设置邮件已发送的cookie
		// }

		$('#j-body-header-text-ip').html(returnCitySN["cip"]+','+returnCitySN["cname"]);	// 页面ip显示
		Menu.main();									// 菜单动画
		TempldatesShow.main()							// 管理组件加载
	};
})();
