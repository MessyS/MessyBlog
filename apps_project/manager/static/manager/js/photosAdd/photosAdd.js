(function () {
	'use strtic';

	$('#s-imgF-photos').change(function () {
		// 每次重选之前清空已展示图片
		$('.img-cont').empty();

		if(this.files.length >= 10){
		$(this).val('');
		alert('抱歉!一次最多可上传10张图片')
		}else{
			let sizeAll = 0;
			for(var i=0;i<this.files.length;i++){
				let file = this.files[i];

				// 图片类型过滤
				var imageType = /^image\//;
				if (!imageType.test(file.type)) {
					alert('文件：' + file.name + '不是图片，请选择图片！');
					continue;
				}
				sizeAll += file.size
			}
			let sizeAllMb = (sizeAll / 1024 / 1024).toFixed(2);
			console.log(sizeAllMb);
			if(parseInt(sizeAllMb) > 50){
				alert('抱歉，图片总大小不能超过50MB')
			}else{
				// 大小通过则展示展示图片在网页中
				for(var i=0;i<this.files.length;i++) {
					let file = this.files[i];
					// 图片实时展示
					var div = document.createElement('div');
					$('.img-cont').append(div);
					let reader = new FileReader();
					reader.onload = (function (div) {
					return function (e) {
						div.style.cssText = `
							display:inline-block;
							margin:15px;
							height:300px;
							width:300px;
							box-shadow: 0 2px 5px 2px rgba(0,0,0,.3);
							background:url(${e.target.result});
							background-size:cover;
							background-position:center;
						`;
					}
					})(div);
					reader.readAsDataURL(file);
				}
			}
			}
		});

	$('#j-add-photos').on('click',function(){
		$(".g-body-photosAdd-meg").html('<div style="color:#f0ad4e">数据发送中...</div>')

		let formData = new FormData;
		let photoFiles = document.getElementById("s-imgF-photos").files;
		for(var i=0;i<photoFiles.length;i++){
		formData.append('imgF',photoFiles[i]);
		}

		$.ajax({
			url: '/addPhotos/',
			type: 'POST',
			contentType:false,
			processData:false,
			headers:{
				"X-CSRFToken":$.cookie('csrftoken')
			},
			data:formData,
			success: function () {
				$('.g-body-photosAdd-meg').html(`<div style="color:#19b955">图片发布成功!</div>`)
			},
			error:function(){
				$('.g-body-photosAdd-meg').html(`<div style="color:#c9302c">服务器数据处理失败，详情查看服务器日志!</div>`)
			}
		});
	});
}())