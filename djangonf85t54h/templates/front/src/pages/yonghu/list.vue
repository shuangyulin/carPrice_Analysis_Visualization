<template>
	<div>
		<div class="breadcrumb-preview">
			<el-breadcrumb :separator="''">
				<el-breadcrumb-item class="item1" to="/"><a>首页</a></el-breadcrumb-item>
				<el-breadcrumb-item class="item2" v-for="(item, index) in breadcrumbItem" :key="index"><a>{{item.name}}</a></el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div v-if="centerType" class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">
				<span class="icon iconfont icon-jiantou33"></span>
				<span class="text">返回</span>
			</el-button>
		</div>
		<div class="list-preview">
			<el-form :inline="true" :model="formSearch" class="list-form-pv">
				<el-form-item class="list-item">
					<div class="lable">用户账号：</div>
					<el-input v-model="formSearch.yonghuzhanghao" placeholder="用户账号" @keydown.enter.native="getList(1, curFenlei)" clearable></el-input>
				</el-form-item>
				<el-button class="list-search-btn" v-if=" true " type="primary" @click="getList(1, curFenlei)">
					<i class="el-icon-search"></i>
					查询
				</el-button>
				<el-button class="list-add-btn" v-if="btnAuth('yonghu','新增')" type="primary" @click="add('/index/yonghuAdd')">
					<i class="el-icon-circle-plus-outline"></i>
					添加
				</el-button>
			</el-form>
			<div class="select2">
				<div class="select2-list" v-for="(item,index) in selectOptionsList" :key="index">
					<div class="label">{{item.name}}：</div>
					<div class="item-body">
						<div class="item" @click="selectClick2(item,-1)" :class="item.check ==-1 ? 'active' : ''">全部</div>
						<div class="item" @click="selectClick2(item,index1)" :class="item.check == index1 ? 'active' : ''" v-for="item1,index1 in item.list" :key="index1">{{item1}}</div>
					</div>
				</div>
			</div>
			<div class="list">
				<div class="list5">
					<div v-for="(item,index) in dataList" :key="index" class="list-item" @click.stop="toDetail(item)">
						<div class="imgbox">
							<img @click.stop="imgPreView(item.touxiang)" v-if="item.touxiang && item.touxiang.substr(0,4)=='http'&&item.touxiang.split(',w').length>1" :src="item.touxiang" class="image" />
							<img @click.stop="imgPreView(item.touxiang.split(',')[0])" v-else-if="item.touxiang && item.touxiang.substr(0,4)=='http'" :src="item.touxiang.split(',')[0]" class="image" />
							<img @click.stop="imgPreView(baseUrl + (item.touxiang?item.touxiang.split(',')[0]:''))" v-else :src="baseUrl + (item.touxiang?item.touxiang.split(',')[0]:'')" class="image" />
						</div>
						<div class="infoBox">
							<div class="bottomInfo">
								<div class="time_item">
									<span class="icon iconfont icon-shijian21"></span>
									<span class="label">发布时间：</span>
									<span class="text">{{item.addtime.split(' ')[0]}}</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

	
			<el-pagination
				background
				id="pagination"
				class="pagination"
				:pager-count="7"
				:page-size="pageSize"
				prev-text="<"
				next-text=">"
				:hide-on-single-page="true"
				:layout='["total","prev","pager","next"].join()'
				:total="total"
				:page-sizes="pageSizes"
				@current-change="curChange"
				@size-change="sizeChange"
				@prev-click="prevClick"
				@next-click="nextClick"
				></el-pagination>
		</div>
		<el-dialog title="预览图" :visible.sync="previewVisible" width="50%">
			<img :src="previewImg" alt="" style="width: 100%;">
		</el-dialog>
	</div>
</template>
<script>
	export default {
		//数据集合
		data() {
			return {
				selectIndex2: 0,
				selectOptionsList: [],
				layouts: '',
				swiperIndex: -1,
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '用户'
					}
				],
				formSearch: {
					yonghuzhanghao: '',
				},
				fenlei: [],
				feileiColumn: '',
				dataList: [],
				total: 1,
				pageSize: 12,
				pageSizes: [],
				totalPage: 1,
				curFenlei: '全部',
				isPlain: false,
				indexQueryCondition: '',
				timeRange: [],
				centerType:false,
				previewImg: '',
				previewVisible: false,
				sortType: 'id',
				sortOrder: 'desc',
			}
		},
		async created() {
			if(this.$route.query.centerType&&this.$route.query.centerType!=0){
				this.centerType = true
			}
			this.baseUrl = this.$config.baseUrl;
			await this.getFenlei();
			let fenlei = '全部'
			if(this.$route.query.homeFenlei){
				fenlei = this.$route.query.homeFenlei
			}
			this.getList(1, fenlei);
		},
		watch:{
			$route(newValue){
				this.getList(1, newValue.query.homeFenlei);
			}
		},
		//方法集合
		methods: {
			selectClick2(row,index) {
				row.check = index
				if(index == -1){
					this.formSearch[row.tableName] = ''
				}else {
					this.formSearch[row.tableName] = row.list[index]
				}
				this.getList()
			},
			add(path) {
				let query = {}
				if(this.centerType){
					query.centerType = 1
				}
				this.$router.push({path: path,query:query});
			},
			async getFenlei() {
			},
			getList(page, fenlei, ref = '') {
				let params = {
					page,
					limit: this.pageSize,
				};
				let searchWhere = {};
				if (this.formSearch.yonghuzhanghao != '') searchWhere.yonghuzhanghao = '%' + this.formSearch.yonghuzhanghao + '%';
				let user = JSON.parse(localStorage.getItem('sessionForm'))
				if (this.sortType) searchWhere.sort = this.sortType
				if (this.sortOrder) searchWhere.order = this.sortOrder
				this.$http.get(`yonghu/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(res => {
					if (res.data.code == 0) {
						this.dataList = res.data.data.list;
						this.total = Number(res.data.data.total);
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			curChange(page) {
				this.getList(page);
			},
			prevClick(page) {
				this.getList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getList(1);
			},
			nextClick(page) {
				this.getList(page);
			},
			imgPreView(url){
				this.previewImg = url
				this.previewVisible = true
			},
			toDetail(item) {
				let params = {
					id: item.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/yonghuDetail', query: params});
			},
			btnAuth(tableName,key){
				if(this.centerType){
					return this.isBackAuth(tableName,key)
				}else{
					return this.isAuth(tableName,key)
				}
			},
			backClick() {
				this.$router.push({path: '/index/center'});
			},
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.list-preview {
		padding: 0 16%;
		margin: 10px auto;
		align-content: flex-start;
		background: #fff;
		display: flex;
		width: 100%;
		align-items: flex-start;
		position: relative;
		flex-wrap: wrap;
		.list-form-pv {
			padding: 10px;
			background: none;
			display: flex;
			width: 101%;
			align-items: center;
			flex-wrap: wrap;
			height: auto;
			order: 1;
			.list-item {
				margin: 0 10px 10px;
				width: auto;
				/deep/.el-form-item__content {
					display: flex;
				}
				.lable {
					padding: 0 0px;
					color: #9E9E9E;
					white-space: nowrap;
					display: inline-block;
					width: auto;
					font-size: 14px;
					line-height: 42px;
					text-align: right;
				}
				.el-input {
					width: 100%;
				}
				.datetimerange {
					border: 1px solid #B2B2B2;
					border-radius: 30px;
					padding: 3px 10px;
					outline: none;
					background: #fff;
					width: auto;
					justify-content: center;
				}
				.el-input /deep/ .el-input__inner {
					border: 1px solid #B2B2B2;
					border-radius: 20px;
					padding: 0 10px;
					margin: 0;
					outline: none;
					color: #333;
					width: 100%;
					font-size: 14px;
					line-height: 42px;
					height: 42px;
				}
				.el-select {
					width: 100%;
				}
				.el-select /deep/ .el-input__inner {
				}
				.el-date-editor {
					width: 100%;
				}
				.el-date-editor /deep/ .el-input__inner {
					border: 1px solid #B2B2B2;
					border-radius: 30px;
					padding: 0 0px 0 30px;
					margin: 0;
					outline: none;
					color: #333;
					width: 100%;
					font-size: 14px;
					line-height: 42px;
					height: 42px;
				}
			}
			.list-search-btn {
				cursor: pointer;
				border: 0;
				border-radius: 30px;
				padding: 0px 15px;
				margin: 0 10px 10px;
				outline: none;
				color: #fff;
				background: #BBB09B;
				width: auto;
				font-size: 14px;
				line-height: 42px;
				height: 42px;
				i {
					margin: 0 10px 0 0;
					color: #fff;
					font-size: 14px;
				}
			}
			.list-add-btn {
				cursor: pointer;
				border: 0;
				border-radius: 30px;
				padding: 0px 15px;
				margin: 0 10px 10px;
				outline: none;
				color: #BBB09B;
				background: #F3EFE7;
				width: auto;
				font-size: 14px;
				line-height: 42px;
				height: 42px;
				i {
					margin: 0 10px 0 0;
					color: inherit;
					font-size: inherit;
				}
			}
		}
		.select2 {
			border: 3px solid #BBB09B;
			border-radius: 30px;
			padding: 10px 20px;
			background: #fff;
			width: 100%;
			height: auto;
			order: 2;
			.select2-list {
				border: 1px solid #BBB09B;
				border-radius: 30px;
				padding: 8px 0;
				margin: 10px 0;
				background: #F3EFE7;
				display: flex;
				width: 100%;
				position: relative;
				height: auto;
				.label {
					padding: 0 5px;
					color: #000;
					display: inline-block;
					width: 120px;
					font-size: 14px;
					line-height: 32px;
				}
				.item-body {
					display: flex;
					width: 100%;
					flex-wrap: wrap;
					height: auto;
					.item {
						cursor: pointer;
						border-radius: 4px;
						padding: 0 20px;
						color: #000;
						background: none;
						font-size: 14px;
						line-height: 32px;
					}
					.item:hover {
						background-size: 100% 100%;
						color: #fff;
						background: url(http://codegen.caihongy.cn/20241207/fb81969a60fe4753916f2a29316c041e.png) center center/cover;
					}
					.item.active {
						background-size: 100% 100%;
						color: #fff;
						background: url(http://codegen.caihongy.cn/20241207/fb81969a60fe4753916f2a29316c041e.png) center center/cover;
					}
				}
			}
		}
		.list {
			padding: 0;
			margin: 0 0 10px;
			background: #fff;
			flex: 1;
			width: calc(100% - 190px);
			order: 4;
			.index-pv1 .animation-box {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				z-index: initial;
			}
				
			.index-pv1 .animation-box:hover {
				transform: rotate(0) scale(1.2) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
				z-index: 1;
			}
				
			.index-pv1 .animation-box img {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
			}
			
			.index-pv1 .animation-box img:hover {
				transform: rotate(0) scale(0.8) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
			}
			.list5 {
				margin: 0px auto;
				display: flex;
				width: 100%;
				flex-wrap: wrap;
				.list-item {
					border: 1px solid #BBB09B;
					border-radius: 10px;
					padding: 10px;
					margin: 0 10px 20px;
					overflow: hidden;
					background: #fff;
					display: block;
					width: calc(25% - 20px);
					position: relative;
					.imgbox {
						border-radius: 10px;
						overflow: hidden;
						width: 100%;
						height: auto;
						.image {
							filter: saturate(150%);
							transform: rotate(0deg);
							object-fit: cover;
							display: block;
							width: 100%;
							opacity: 0.9;
							height: 200px;
						}
					}
					.infoBox {
						padding: 10px 0;
						left: 0px;
						bottom: 0;
						background: none;
						display: flex;
						width: 100%;
						font-size: 14px;
						position: inherit;
						flex-wrap: wrap;
						transition: all 0.5s;
						.name {
							color: #000;
							width: 100%;
							font-size: 16px;
							line-height: 1.5;
							order: 1;
						}
						.price {
							color: #D90000;
							width: 100%;
							font-size: 13px;
							order: 2;
							.price_text {
								color: #D90000;
								font-size: 24px;
							}
						}
						.bottomInfo {
							display: flex;
							flex-wrap: wrap;
							order: 3;
							.time_item {
								padding: 0;
								width: 100%;
								order: 5;
								.icon {
									margin: 0 2px 0 0;
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.label {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.text {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
							}
							.publisher_item {
								padding: 0;
								width: 100%;
								order: 4;
								.icon {
									margin: 0 2px 0 0;
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.label {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.text {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
							}
							.like_item {
								padding: 0;
								width: 100%;
								order: 3;
								.icon {
									margin: 0 2px 0 0;
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.label {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.text {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
							}
							.collect_item {
								padding: 0;
								width: 100%;
								order: 2;
								.icon {
									margin: 0 2px 0 0;
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.label {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.text {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
							}
							.view_item {
								padding: 0;
								width: 100%;
								order: 1;
								.icon {
									margin: 0 2px 0 0;
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.label {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
								.text {
									color: #000;
									font-size: 12px;
									line-height: 25px;
								}
							}
						}
					}
				}
				.list-item:hover {
					background: linear-gradient( 357deg, #F3EFE7 0%, #FFFFFF 100%);
					.imgbox {
						.image {
							transform: scale(1.05);
							ilter: saturate(100%);
							opacity: 1;
							transition: all 200ms linear;
						}
					}
					.infoBox {
						bottom: 0px;
						background: none;
						font-size: 14px;
						.name {
							color: #1B4955;
							font-size: 16px;
						}
						.price {
							color: #D90000;
							.price_text {
								font-weight: bold;
							}
						}
						.bottomInfo {
							display: flex;
							flex-wrap: wrap;
							order: 3;
							.time_item {
								.icon {
									color: #1B4955;
								}
								.label {
									color: #1B4955;
								}
								.text {
									color: #1B4955;
								}
							}
							.publisher_item {
								.icon {
									color: #1B4955;
								}
								.label {
									color: #1B4955;
								}
								.text {
									color: #1B4955;
								}
							}
							.like_item {
								.icon {
									color: #1B4955;
								}
								.label {
									color: #1B4955;
								}
								.text {
									color: #1B4955;
								}
							}
							.collect_item {
								.icon {
									color: #1B4955;
								}
								.label {
									color: #1B4955;
								}
								.text {
									color: #1B4955;
								}
							}
							.view_item {
								.icon {
									color: #1B4955;
								}
								.label {
									color: #1B4955;
								}
								.text {
									color: #1B4955;
								}
							}
						}
					}
				}
			}
		}
	}
</style>
