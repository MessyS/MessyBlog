(function(){
	'use strict';

	// **************************  全局函数的定义   ************************
	// 暂时弃用发送邮件功能
	function emailSend(){
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
	}

	// ******************************  路由管理   *************************
	const routes = [
		{
			path: '/',
			meta:{title:'资源概览'},
			component:{
				template:'#serverOverView',
			}
		},
		{
			path: '/serverOperation',
			meta:{title:'系统操作'},
			component:{
				template:'#serverOperation',
			}
		},
		{
			path: '/articlesImportMDApp',
			meta:{title:'导入MD(APP)'},
			component:{
				template:'#articlesImportMDApp',
			}
		},
		{
			path: '/articlesImportMDHtml',
			meta:{title:'导入MD(HTML)'},
			component:{
				template:'#articlesImportMDHtml',
			}
		},
		{
			path: '/goodBoyList',
			meta:{title:'鸣谢列表'},
			component:{
				template:'#goodBoyList',
			}
		},
		{
			path: '/photosAdd',
			meta:{title:'上传图片'},
			component:{
				template:'#photosAdd',
			}
		},
		{
			path: '/photosList',
			meta:{title:'图片管理'},
			component:{
				template:'#photosList',
			}
		},
	];
	const router = new VueRouter({
		routes: routes
	});
	
	const app = new Vue({
		el:'.g-all',
		router:router,
	});

	// ****************************   初始加载  *************************

	// 实时IP显示
	$('#j-body-header-text-ip').html(returnCitySN["cip"]+','+returnCitySN["cname"])

	// 菜单动画
	$('.g-framework-left-options-all').click(function(e){
		e.preventDefault();
		$(this).find('.g-framework-left-options-list-open').toggleClass('g-framework-left-options-list-open-active');
		$(this).find('.g-framework-left-options-list').toggleClass('g-framework-left-options-list-active');
		$(this).find('.g-framework-left-options-options-block').slideToggle(500)
	})
})();