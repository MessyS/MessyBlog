$('#map').vectorMap({
	map: 'cn_mill',

	backgroundColor: 'transparent',
	zoomMin: 0.9,
	zoomMax: 2.4,
	focusOn: {
		x: 0.55,
		y: 2,
		scale: 0.9
	},
	regionStyle: {
		initial: {
			fill: '#d2d6de',
		},
		hover: {
			fill: '#EAEAEA',
		},
		selectedHover: {}
	},
	markers: [
		// {latLng: [经度（保留两位小数）, 纬度（保留两位小数）], name: '城市名称'},
		// 推荐查询经纬度网站：http://www.gpsspg.com/maps.htm

		{latLng: [29.56 ,106.55], name: '重庆'},
		{latLng: [39.90, 116.41], name: '北京'},
		{latLng: [31.24, 121.50], name: '上海'},
		{latLng: [46.06, 122.06], name: '内蒙古 - 乌兰浩特'}
		],
		markerStyle: {
		initial: {
			fill: '#fd2020', // 足迹位置的填充颜色
			stroke: '#fff'   // 足迹位置的描边颜色
		},
		hover: {
			fill: '#fd2020', // 鼠标滑动至足迹位置后的填充颜色
			stroke: '#fff',  // 鼠标滑动至足迹位置后的描边颜色
			"fill-opacity": 0.8
		},
	},
});