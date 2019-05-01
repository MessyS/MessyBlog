(function(){
	'use strtic';

	$("#j-vesting").on('click',function(){
		var nums = $('#j-vesting-val').val();
		if(nums){
			var g = /^[0-9]*[0-9][0-9]*$/;
			if(g.test(nums) || nums == 'All' || nums == 'all'){
			  var confirma = confirm('确认查询吗？');
			  if(confirma){
				$('.g-body-commonOperations-body-vesting-body-plan').show();
				 $('.g-body-commonOperations-body-vesting-body-prompt-waitting').show();
				$.ajax({
					url: '/ip_address/',
					type: 'POST',
					headers:{
					  "X-CSRFToken":$.cookie('csrftoken')
					},
					data: {
					  'nums':nums
					},
					success: function (data) {
					  console.log(data);
					  $(".g-body-commonOperations-body-vesting-body-prompt-waitting").empty();
					  if(parseInt(data) == 2){
						$(".g-body-commonOperations-body-vesting-body-prompt-success").html('数据量过大，已放入后台执行');
						$(".g-body-commonOperations-body-vesting-body-prompt-success").show();
					  }else{
						$(".g-body-commonOperations-body-vesting-body-prompt-success").show();
					  }
					}
				});
			  }
			} else{
			  alert('请输入正整数!');
			}
		}else{
			alert('请输入查询的数量')
	  }
	});

	// 后端记得做一个邮件确认的功能
	$("#j-reboot").on('click',function(){
		var confirmb = confirm('确认重启吗？');
		if(confirmb){
			$('.g-body-systemOperation-body-vesting-body-waitting').html('请求发送中...请稍后');
			$('.g-body-systemOperation-body-vesting-body-waitting').show();
		$.ajax({
			url: '/reboot/',
			type: 'POST',
			headers:{
			  "X-CSRFToken":$.cookie('csrftoken')
			},
			success: function (data) {
			  $(".g-body-systemOperation-body-vesting-body-waitting").html(data);
			  $(".g-body-systemOperation-body-vesting-body-waitting").show();
			  $(".g-body-systemOperation-body-reboot-body-prompt-success").show();
			}
		});
		}
	})
}())