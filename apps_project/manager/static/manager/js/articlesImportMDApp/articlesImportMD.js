(function(){
		'use strtic';
		
		$('#s-imgF').change(function () {
			createReader = function(file, whenReady) {
				var reader = new FileReader;
				reader.onload = function (evt) {
					var image = new Image();
					image.onload = function () {
						var width = this.width;
						var height = this.height;
						if (whenReady) whenReady(width, height);
					};
					image.src = evt.target.result;
				};
				reader.readAsDataURL(file);
			}
			var file = document.getElementById('s-imgF');
			createReader(file.files[0], function (w, h) {
				x = w;
				y = h;
			});
		});

		$("#s-publishedArticles").on('click',function(){
				$chkBoxes = $('.g-body-importMD').find('input:checked');
				if ($chkBoxes.length == 0) {
					alert('请至少选择一个分类');     // 如果不勾选弹出警告
					return false;
				} else {
				var confirmb = confirm('确认发布吗？');
				if (confirmb) {
				var reader = new FileReader();
				var formData = new FormData();
				// 获取用户上传文件的信息（html表单）
				var formDataOld = new FormData($('.g-body-importMD')[0]);
				var fileHtml = formDataOld.get('htmlF');
				// 获取文章分类
				$("input:checkbox[name=category]:checked").each(function (i) {
						formData.append('categoryList',$(this).val());
				});
				// 获取文章标题
				var fileTitle = fileHtml.name.replace('.html', '');

				// 加入所有附属图片到自构建表单内
				var photoFiles = document.getElementById("s-imgF").files;
				for(var i=0;i<photoFiles.length;i++){
						formData.append('imgF',photoFiles[i]);
						formData.append('x',x);
						formData.append('y',y);
				}

				// 获取文章内容
				reader.readAsText(fileHtml, 'UTF-8');
				reader.onload = function () {
						var fileContext = this.result;
						// 新数据加入表单
						formData.append('fileTitleH', fileTitle);
						formData.append('fileContextH', fileContext);

						$('.g-body-importMD-status').html('文章数据发送中...请稍后');
						$('.g-body-importMD-status').show();
						$.ajax({
						url: '/addHF_article/',
						type: 'POST',
						processData: false, // 不处理数据
						contentType: false,  // 不设置内容类型
						headers: {
						"X-CSRFToken": $.cookie('csrftoken')
						},
						data: formData,
						success: function (data) {
						$('.g-body-importMD-status').empty();
						$('.g-body-importMD-status').html('<div style="color:#19b955">【' + fileTitle + '】发布成功！</div>');

						$('#s-htmlF').val('')
						$('#s-imgF').val('')
						},
						error: function () {
						$('.g-body-importMD-status').empty();
						$('.g-body-importMD-status').html('<div style="color:#c9302c">服务器数据处理失败，详情查看服务器日志</div>');
						}
						});
				};
				}
				}
			});
}())