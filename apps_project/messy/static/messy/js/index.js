/*
 * @Author: Messy
 * @AuthorEmail: messygao@qq.com
 * @AuthorSite: https://www.messys.top
 * @Date: 2019-01-24 12:18:10
 * @LastEditTime: 2019-05-07 14:46:04
 */
(function(){
	'use strtic';

	window.onload = function(){
		// 进入主页动画
		$('.g-headers-scroll').click(function () {
			let bodyTop = $('.g-body').position().top;
			$('body,html').animate({scrollTop:bodyTop},1000);
			return false;;
		})

		//轮播图片加载
		function photoShowLoad(){
			$.ajax({
				type: "GET",
				url: "/randomPhotos/",
				success: function (data) {
				    var j = 0;
					for(var i=2;i<=5;i++){
					    $(`.g-headers-slideShow-${i}`).css('background',`url(${data[j]})`);
                        j += 1
                    }
				},
				error: function () {
				    var j = 0;
					for(var i=2;i<=5;i++){
					    $(`.g-headers-slideShow-${i}`).html('请求数据失败，请刷新重试！');
                        j += 1
                    }
				}
			});
		}

		// 轮播图图片点击放大
		function photoShow(){
			$('.g-headers-slideShow-block div').click(function(){
				let bgi = $(this).css('background').replace('rgba(0, 0, 0, 0) url("','').replace('") repeat scroll 50% 50% / cover padding-box border-box','');
				$('.g-headers-slideShow-show-img').attr('src',bgi);
				$('.g-headers-slideShow-show').fadeIn(500)
			})
		}

		photoShowLoad();	// 轮播图异步加载
		photoShow();		// 轮播图放大查看
	}
}());