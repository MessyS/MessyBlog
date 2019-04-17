/*
 * @Author: Messy
 * @AuthorEmail: messygao@qq.com
 * @AuthorSite: https://www.messys.top
 * @Date: 2019-01-24 12:18:10
 * @LastEditTime: 2019-04-16 16:57:26
 */
(function(){
	'use strtic';

	window.onload = function(){
		// 进入主页动画
		$('.g-headers-scroll').click(function () {
			let bodyTop = $('.g-body').position().top
			$('body,html').animate({scrollTop:bodyTop},1000);
			return false;;
		})

			//轮播图片加载
			function photoShowLoad(){
				// 后端接口返回photo url
				// $.ajax({
				// 	type: "POST",
				// 	url: "/randomPhotos/",
				// 	success: function (data) {
				// 		console.log(data)
				// 	}
				// });
	
				// 暂时性前端代替
				for(var i=2;i<=5;i++){
					$(`.g-headers-slideShow-${i}`).css('background',`url(resources/messy/img/index/${i}.jpg)`)
				}
			}
	
			// 轮播图图片点击放大
			function photoShow(){
				$('.g-headers-slideShow-block div').click(function(){
					let bgi = $(this).css('background').replace('rgba(0, 0, 0, 0) url("','').replace('") repeat scroll 50% 50% / cover padding-box border-box','');
					$('.g-headers-slideShow-show-img').attr('src',bgi);
					$('.g-headers-slideShow-show').fadeIn(500)
				})
			}
		
		// 侧边栏固定判断
		function slideBarFixed(){
			let winTop = $(window).scrollTop()
			let bodyTop = $('.g-body').position().top

			if($(window).width() > 1000){
				if(winTop > bodyTop){
					$('.g-body-slideBar').css({
						'position': 'fixed',
						'top': '0',
					})
				}else{
					$('.g-body-slideBar').css({
						'position': 'relative',
						'top': '-25px',
					})
				}
			}
		}

		photoShowLoad()	// 轮播图异步加载
		photoShow()		// 轮播图放大查看

		// 初始、页面大小改变、滚动时判断是否需要固定侧边栏
		slideBarFixed()
		$(window).resize(function(){slideBarFixed()})
		$(window).scroll(function(){slideBarFixed()})
	}
}())