<template>
	<div>
	<!--  -->
		<div class="breadcrumb-preview">
			<el-breadcrumb :separator="''">
				<el-breadcrumb-item class="item1" to="/"><a>首页</a></el-breadcrumb-item>
				<el-breadcrumb-item class="item2" v-for="(item, index) in breadcrumbItem" :key="index" :to="'/index/tichexinxi?centerType=' + (centerType?'1':'0')"><a>{{item.name}}</a></el-breadcrumb-item>
				<el-breadcrumb-item class="item3"><a href="javascript:void(0);">详情</a></el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">
				<span class="icon iconfont icon-jiantou33"></span>
				<span class="text">返回</span>
			</el-button>
		</div>
		<div class="detail-preview">
			<div class="attr">
				<div class="info">
					<div class="title-item">
						<div class="detail-title">
							{{detail.tichebianhao}}
						</div>
					</div>
					<div class="item">
						<div class="lable">汽车名称</div>
						<div class="text "  >{{detail.qichemingcheng}}</div>
					</div>
					<div class="item">
						<div class="lable">汽车品牌</div>
						<div class="text "  >{{detail.qichepinpai}}</div>
					</div>
					<div class="item">
						<div class="lable">汽车类型</div>
						<div class="text "  >{{detail.qicheleixing}}</div>
					</div>
					<div class="item">
						<div class="lable">售价</div>
						<div class="text "  >{{detail.shoujia}}</div>
					</div>
					<div class="item">
						<div class="lable">天窗</div>
						<div class="text "  >{{detail.tianchuang}}</div>
					</div>
					<div class="item">
						<div class="lable">座位</div>
						<div class="text "  >{{detail.zuowei}}</div>
					</div>
					<div class="item">
						<div class="lable">汽车排量</div>
						<div class="text "  >{{detail.qichepailiang}}</div>
					</div>
					<div class="item">
						<div class="lable">上市年份</div>
						<div class="text "  >{{detail.shangshinianfen}}</div>
					</div>
					<div class="item">
						<div class="lable">提车时间</div>
						<div class="text "  >{{detail.ticheshijian}}</div>
					</div>
					<div class="item">
						<div class="lable">用户账号</div>
						<div class="text "  >{{detail.yonghuzhanghao}}</div>
					</div>
					<div class="item">
						<div class="lable">用户姓名</div>
						<div class="text "  >{{detail.yonghuxingming}}</div>
					</div>
					<div class="btn_box">
						<el-button class="editBtn" v-if="btnAuth('tichexinxi','修改')" @click="editClick">修改</el-button>
						<el-button class="delBtn" v-if="btnAuth('tichexinxi','删除')" @click="delClick">删除</el-button>
					</div>
				</div>
			</div>
		
			<div class="swiper3" v-if="detailBanner.length">
				<div class="big">
					<img id="big" :src="swiperBigUrl" class="image">
				</div>
				<div class="samll">
					<div class="swiper3-small-item" v-for="item in detailBanner" :key="item.id">
						<img v-if="item.substr(0,4)=='http'" :src="item" @click="swiperClick3(item)" class="image">
						<img v-else :src="baseUrl + item" @click="swiperClick3(baseUrl + item)" class="image">
					</div>
				</div>
			</div>


		

			<el-tabs class="detail-tabs" v-model="activeName" type="border-card" v-if="tabsNum>0" >
			</el-tabs>

		</div>
		<div class="share_view">
		</div>
	</div>
</template>

<script>
	import axios from 'axios'
	import Swiper from "swiper";
	export default {
		//数据集合
		data() {
			return {
				tablename: 'tichexinxi',
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '提车信息'
					}
				],
				title: '',
				detailBanner: [],
				userid: Number(localStorage.getItem('frontUserid')),
				id: 0,
				detail: {},
				tabsNum: 0,
				activeName: 'first',
				total: 1,
				pageSize: 10,
				totalPage: 1,
				buynumber: 1,
				centerType: false,
				storeupType: false,
				shareUrl: location.href,
				swiperBigUrl: null,
			}
		},
		created() {
			if(this.$route.query.centerType&&this.$route.query.centerType!=0) {
				this.centerType = true
			}
			if(this.$route.query.storeupType&&this.$route.query.storeupType!=0) {
				this.storeupType = true
			}
			
			this.init();
		},
		mounted() {
		},
		//方法集合
		methods: {
			swiperClick3(src) {
				this.swiperBigUrl = src
			},
			init() {
				this.id = this.$route.query.id
				this.baseUrl = this.$config.baseUrl;
				this.$http.get(this.tablename + '/detail/'  + this.id, {}).then(res => {
					if (res.data.code == 0) {
						this.detail = res.data.data;
						this.title = this.detail.tichebianhao;
						if(this.detail.qichetupian) {
							this.detailBanner = this.detail.qichetupian.split(",w").length>1?[this.detail.qichetupian]:this.detail.qichetupian.split(',');
						}
						this.$forceUpdate();
						if(localStorage.getItem('frontToken')){
						}

					}
					if (this.detailBanner.length) {
						if (this.detailBanner[0].substr(0,4)=='http') {
							this.swiperBigUrl = this.detailBanner[0]
						} else {
							this.swiperBigUrl = this.baseUrl + this.detailBanner[0]
						}
					}
				});
			},
			curChange(page) {
				this.getDiscussList(page);
			},
			prevClick(page) {
				this.getDiscussList(page);
			},
			nextClick(page) {
				this.getDiscussList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getDiscussList(1);
			},
			// 返回按钮
			backClick(){
				if(this.storeupType){
					history.back()
				}else{
					let params = {}
					if(this.centerType){
						params.centerType = 1
					}
					this.$router.push({path: '/index/tichexinxi', query: params});
				}
			},
			// 下载
			download(file ){
				if(!file) {
					this.$message({
						type: 'error',
						message: '文件不存在',
						duration: 1500,
					});
					return;
				}
				let arr = file.replace(new RegExp('upload/', "g"), "")
				axios.get(this.baseUrl + '/file/download?fileName=' + arr, {
					headers: {
						token: localStorage.getItem("frontToken")
					},
					responseType: "blob"
				}).then(({
					data
				}) => {
					const binaryData = [];
					binaryData.push(data);
					const objectUrl = window.URL.createObjectURL(new Blob(binaryData, {
						type: 'application/pdf;chartset=UTF-8'
					}))
					const a = document.createElement('a')
					a.href = objectUrl
					a.download = arr
					// a.click()
					// 下面这个写法兼容火狐
					a.dispatchEvent(new MouseEvent('click', {
						bubbles: true,
						cancelable: true,
						view: window
					}))
					window.URL.revokeObjectURL(data)
				},err=>{
					axios.get((location.href.split(this.$config.name).length>1 ? location.href.split(this.$config.name)[0] :'') + this.$config.name + '/file/download?fileName=' + arr, {
						headers: {
							token: localStorage.getItem("frontToken")
						},
						responseType: "blob"
					}).then(({
						data
					}) => {
						const binaryData = [];
						binaryData.push(data);
						const objectUrl = window.URL.createObjectURL(new Blob(binaryData, {
							type: 'application/pdf;chartset=UTF-8'
						}))
						const a = document.createElement('a')
						a.href = objectUrl
						a.download = arr
						// a.click()
						// 下面这个写法兼容火狐
						a.dispatchEvent(new MouseEvent('click', {
							bubbles: true,
							cancelable: true,
							view: window
						}))
						window.URL.revokeObjectURL(data)
					})
				})
			},


			// 权限判断
			btnAuth(tableName,key){
				if(this.centerType){
					return this.isBackAuth(tableName,key)
				}else{
					return this.isAuth(tableName,key)
				}
			},
			// 修改
			editClick(){
				this.$router.push(`/index/tichexinxiAdd?type=edit&&id=${this.detail.id}`);
			},
			// 删除
			async delClick(){
				await this.$confirm('是否删除此提车信息？') .then(_ => {
					this.$http.post('tichexinxi/delete', [this.detail.id]).then(async res => {
						if (res.data.code == 0) {
							this.$message({
								type: 'success',
								message: '删除成功!',
								duration: 1500,
								onClose: () => {
									history.back()
								}
							});
						}
					});
				}).catch(_ => {});
			},
		},
		components: {
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.detail-preview {
		padding: 0 16% 20px;
		margin: 10px auto;
		display: flex;
		width: 100%;
		position: relative;
		flex-wrap: wrap;
		.attr {
			padding: 0;
			background: none;
			display: flex;
			width: 100%;
			position: relative;
			order: 3;
			.info {
				padding: 10px 0;
				margin: 0;
				background: #fff;
				flex: 1;
				display: flex;
				justify-content: space-between;
				flex-wrap: wrap;
				.title-item {
					border: 1px solid #BBB09B;
					border-radius: 35px;
					padding: 5px 20px;
					margin: 0 0 10px 0;
					background: #F3EFE7;
					display: flex;
					width: 48%;
					justify-content: space-between;
					align-items: center;
					.detail-title {
						color: #000;
						font-weight: bold;
						font-size: 16px;
					}
				}
				.item {
					border: 1px solid #BBB09B;
					border-radius: 30px;
					padding: 5px 20px;
					margin: 0 0 10px 0;
					background: #F3EFE7;
					display: flex;
					width: 48%;
					justify-content: spaceBetween;
					align-items: center;
					.lable {
						padding: 0 10px;
						color: #BBB09B;
						white-space: nowrap;
						width: 90px;
						font-size: 15px;
						line-height: 40px;
						text-align: right;
						height: auto;
					}
					.text {
						padding: 0 10px;
						color: #BBB09B;
						flex: 1;
						font-size: 14px;
						line-height: 24px;
						height: auto;
					}
					.price {
						color: #f00;
					}
					.bold {
						font-weight: bold;
					}
					.link {
						cursor: pointer;
						text-decoration: underline;
					}
				}
				.btn_box {
					padding: 10px 0;
					margin: 0 0 20px;
					display: flex;
					width: 100%;
					align-items: center;
					flex-wrap: wrap;
				}
				.editBtn {
					border: 0;
					cursor: pointer;
					border-radius: 0;
					padding: 0 10px;
					margin: 0 5px 0 0;
					outline: none;
					color: #fff;
					background: #B3B685;
					width: auto;
					font-size: 14px;
					line-height: 35px;
					height: 35px;
				}
				.editBtn:hover {
					opacity: 0.5;
				}
				.delBtn {
					border: 0;
					cursor: pointer;
					border-radius: 0;
					padding: 0 10px;
					margin: 0 5px 0 0;
					outline: none;
					color: #fff;
					background: #8F7F58;
					width: auto;
					font-size: 14px;
					line-height: 35px;
					height: 35px;
				}
				.delBtn:hover {
					opacity: 0.5;
				}
			}
		}
		.swiper3 {
			background: #fff;
			display: flex;
			width: 100%;
			height: auto;
			order: 1;
			.big {
				margin: 0 0 10px;
				background: #fff;
				width: 80%;
				position: relative;
				height: 500px;
				img {
					object-fit: cover;
					display: block;
					width: 100%;
					height: 100%;
				}
			}
			.samll {
				padding: 0 0 0 20px;
				flex-direction: column;
				background: #fff;
				display: flex;
				width: 20%;
				height: 100%;
				.swiper3-small-item {
					margin: 0 0 10px;
					flex: 1;
					background: #fff;
					position: relative;
					height: 100%;
					img {
						object-fit: cover;
						display: block;
						width: 100%;
						position: absolute;
						height: 100%;
					}
				}
			}
		}
		.detail-tabs {
			border: 1px solid #BBB09B;
			border-radius: 30px;
			box-shadow: 0 0px 0px 0 rgba(0, 0, 0, .1);
			padding: 15px;
			background: none;
			width: 100%;
			order: 5;
			& /deep/ .el-tabs__header .el-tabs__nav-wrap {
				margin-bottom: 0;
			}
			/deep/ .el-tabs__header {
				border-radius: 30px;
				padding: 5px 10px;
				margin: 0;
				background: #F3EFE7;
				border-color: #BBB09B;
				border-width: 1px;
				border-style: solid;
			}
			
			/deep/ .el-tabs__header .el-tabs__item {
				border: 0;
				padding: 0 20px 0 10px ;
				margin: 0 10px;
				color: #999;
				font-weight: 500;
				display: inline-block;
				font-size: 14px;
				line-height: 40px;
				background: transparent;
				width: 100px;
				position: relative;
				list-style: none;
				text-align: center;
				height: 40px;
			}
			
			/deep/ .el-tabs__header .el-tabs__item:hover {
				border: 0;
				padding: 0 20px 0 10px ;
				margin: 0 10px;
				background-size: 100% 100%;
				color: #fff;
				background: url(http://codegen.caihongy.cn/20241207/fb81969a60fe4753916f2a29316c041e.png) center center/cover;
				width: 100px;
				text-align: center;
			}
			
			/deep/ .el-tabs__header .el-tabs__item.is-active {
				border: 0;
				padding: 0 20px 0 10px ;
				margin: 0 10px;
				background-size: 100% 100%;
				color: #fff;
				background: url(http://codegen.caihongy.cn/20241207/fb81969a60fe4753916f2a29316c041e.png) center center/cover;
				width: 100px;
				text-align: center;
			}
			
			/deep/ .el-tabs__content {
				padding: 15px;
			}
		}
	}
	.share_view{
		box-shadow: 0 1px 6px rgba(0,0,0,.3);
		z-index: 11;
		bottom: 20%;
		background: #fff;
		position: fixed;
		right: 0;
		.share:last-of-type{
			border:none;
		}
	}
</style>
