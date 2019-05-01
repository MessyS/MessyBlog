// ajax默认参数
$.ajaxSetup({
	method:'POST',
	headers:{
		"X-CSRFToken":$.cookie('csrftoken')
	},
})

// 设置服务器返回信息
function serverReturn(el,meg){
	let $meg = el.parent().parent()
	$meg.append(meg)
}

$('.g-body-photosList-block-fun-des').on('click',function(){
	let photoId = $(this).attr('photoId')
	let $this = $(this)

	// 修改框使用服务器内容
	$.ajax({
		url:'/desPhotosSearch/',
		data:{
			'desId':photoId,
		},
		success: function (data) {
			desData = data
		},
		error:function(){
			desData = ''
		}
	});

	let des = prompt('请输入一句话描述...',desData)

	if(des){
		$.ajax({
			url:'/desPhotos/',
			data:{
				'des':des
			},
			success: function (data) {
				data = data.toString()
				if(data == '01'){
					alert('抱歉，没找到该图片的id号，请刷新再试')
				}else if(data == '1'){
					serverReturn($this,`
						<p id='j-body-photosList-block-meg' style='color:#19b955;text-align: center;'>${photoId}号图片描述修改成功！</p>
					`)
				}
				setTimeout(function(){
					$this.parent().parent().find('#j-body-photosList-block-meg').hide();
				},3000)
			},
			error:function(){
				serverReturn($this,`
					<p id='j-body-photosList-block-meg' style='color:red;text-align: center;'>${photoId}号图片修改失败！<br>请稍后刷新重试</p>
				`)
				setTimeout(function(){
					$this.parent().parent().find('#j-body-photosList-block-meg').hide();
				},3000)
			},
		});
	}
})

$('.g-body-photosList-block-fun-del').on('click',function(){
	let confirmAn = confirm('确认删除吗？');
	if(confirmAn){
		let photoId = $(this).attr('photoId');

		let $this = $(this)
		
		$.ajax({
			url:'/delPhotos/',
			data:{
				'photoId':photoId,
			},
			dataType: "dataType",
			success: function (data) {
				data = data.toString()
				if(data == '01'){
					alert('抱歉，没找到该图片的id号，请刷新再试')
				}else if(data == '1'){
					serverReturn($this,`
						<p id='j-body-photosList-block-meg' style='color:#19b955;text-align: center;'>${photoId}号图片删除成功！</p>
					`)
					setTimeout(function(){
						$(this).parent().parent().hide();
					},3000)
				}
			},
			error: function () {
				let $meg = $this.parent().parent()
				serverReturn($this,`
					<p id='j-body-photosList-block-meg' style='color:red;text-align: center;'>${photoId}号图片删除失败！<br>请稍后刷新重试</p>
				`)
				setTimeout(function(){
					$this.parent().parent().find('#j-body-photosList-block-meg').hide();
				},3000)
			},
		});
	}
});