<template>
	<div class="add-update-preview">
		<el-form
			class="add-update-form"
			ref="ruleForm"
			:model="ruleForm"
			:rules="rules"
			label-width="90px"
			>
			<el-form-item class="add-item" label="汽车名称" prop="qichemingcheng">
				<el-input v-model="ruleForm.qichemingcheng" 
					placeholder="汽车名称" clearable :disabled=" false  ||ro.qichemingcheng"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="汽车图片" v-if="type!='cross' || (type=='cross' && !ro.qichetupian)" prop="qichetupian">
				<file-upload
					tip="点击上传汽车图片"
					action="file/upload"
					:limit="3"
					:multiple="true"
					:fileUrls="ruleForm.qichetupian?ruleForm.qichetupian:''"
					@change="qichetupianUploadChange"
					></file-upload>
			</el-form-item>
			<el-form-item class="add-item" v-else label="汽车图片" prop="qichetupian">
				<img v-if="ruleForm.qichetupian.substring(0,4)=='http'" class="upload-img" v-bind:key="index" :src="ruleForm.qichetupian.split(',')[0]">
				<img v-else class="upload-img" v-bind:key="index" v-for="(item,index) in ruleForm.qichetupian.split(',')" :src="baseUrl+item">
			</el-form-item>
			<el-form-item class="add-item"  label="汽车品牌" prop="qichepinpai">
				<el-select v-model="ruleForm.qichepinpai" placeholder="请选择汽车品牌" :disabled=" false  ||ro.qichepinpai" >
					<el-option
						v-for="(item,index) in qichepinpaiOptions"
						:key="index"
						:label="item"
						:value="item">
					</el-option>
				</el-select>
			</el-form-item>
			<el-form-item class="add-item"  label="汽车类型" prop="qicheleixing">
				<el-select v-model="ruleForm.qicheleixing" placeholder="请选择汽车类型" :disabled=" false  ||ro.qicheleixing" >
					<el-option
						v-for="(item,index) in qicheleixingOptions"
						:key="index"
						:label="item"
						:value="item">
					</el-option>
				</el-select>
			</el-form-item>
			<el-form-item class="add-item" label="售价" prop="shoujia">
				<el-input-number v-model="ruleForm.shoujia" placeholder="售价" :disabled=" false ||ro.shoujia"></el-input-number>
			</el-form-item>
			<el-form-item class="add-item" label="库存" prop="kucun">
				<el-input v-model.number="ruleForm.kucun" 
					placeholder="库存" clearable :disabled=" false  ||ro.kucun"></el-input>
			</el-form-item>
			<el-form-item class="add-item"  label="天窗" prop="tianchuang">
				<el-select v-model="ruleForm.tianchuang" placeholder="请选择天窗" :disabled=" false  ||ro.tianchuang" >
					<el-option
						v-for="(item,index) in tianchuangOptions"
						:key="index"
						:label="item"
						:value="item">
					</el-option>
				</el-select>
			</el-form-item>
			<el-form-item class="add-item"  label="座位" prop="zuowei">
				<el-select v-model="ruleForm.zuowei" placeholder="请选择座位" :disabled=" false  ||ro.zuowei" >
					<el-option
						v-for="(item,index) in zuoweiOptions"
						:key="index"
						:label="item"
						:value="item">
					</el-option>
				</el-select>
			</el-form-item>
			<el-form-item class="add-item" label="汽车排量" prop="qichepailiang">
				<el-input v-model="ruleForm.qichepailiang" 
					placeholder="汽车排量" clearable :disabled=" false  ||ro.qichepailiang"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="上市年份" prop="shangshinianfen">
				<el-input v-model="ruleForm.shangshinianfen" 
					placeholder="上市年份" clearable :disabled=" false  ||ro.shangshinianfen"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="汽车详情" prop="qichexiangqing">
				<editor 
					v-model="ruleForm.qichexiangqing" 
					class="editor" 
					myQuillEditor="qichexiangqing"
					action="file/upload">
				</editor>
			</el-form-item>

			<el-form-item class="add-btn-item">
				<el-button class="submitBtn"  type="primary" @click="onSubmit">
					<span class="icon iconfont icon-kaitongfuwu"></span>
					<span class="text">提交</span>
				</el-button>
				<el-button class="closeBtn" @click="back()">
					<span class="icon iconfont icon-shanchu1"></span>
					<span class="text">取消</span>
				</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				id: '',
				baseUrl: '',
				ro:{
					qichemingcheng : false,
					qichetupian : false,
					qichepinpai : false,
					qicheleixing : false,
					shoujia : false,
					kucun : false,
					tianchuang : false,
					zuowei : false,
					qichepailiang : false,
					shangshinianfen : false,
					qichexiangqing : false,
					clicktime : false,
					clicknum : false,
					discussnum : false,
					storeupnum : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					qichemingcheng: '',
					qichetupian: '',
					qichepinpai: '',
					qicheleixing: '',
					shoujia: '',
					kucun: '',
					tianchuang: '',
					zuowei: '',
					qichepailiang: '',
					shangshinianfen: '',
					qichexiangqing: '',
					clicktime: '',
					clicknum: '',
					discussnum: '',
					storeupnum: '',
				},
				qichepinpaiOptions: [],
				qicheleixingOptions: [],
				tianchuangOptions: [],
				zuoweiOptions: [],


				rules: {
					qichemingcheng: [
						{ required: true, message: '汽车名称不能为空', trigger: 'blur' },
					],
					qichetupian: [
					],
					qichepinpai: [
						{ required: true, message: '汽车品牌不能为空', trigger: 'blur' },
					],
					qicheleixing: [
						{ required: true, message: '汽车类型不能为空', trigger: 'blur' },
					],
					shoujia: [
						{ required: true, message: '售价不能为空', trigger: 'blur' },
						{ validator: this.$validate.isNumber, trigger: 'blur' },
					],
					kucun: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					tianchuang: [
					],
					zuowei: [
					],
					qichepailiang: [
					],
					shangshinianfen: [
					],
					qichexiangqing: [
					],
					clicktime: [
					],
					clicknum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					discussnum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					storeupnum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
				},
				centerType: false,
			};
		},
		computed: {



		},
		components: {
		},
		created() {
			if(this.$route.query.centerType){
				this.centerType = true
			}
			//this.bg();
			let type = this.$route.query.type ? this.$route.query.type : '';
			this.init(type);
			this.baseUrl = this.$config.baseUrl;
		},
		methods: {
			getMakeZero(s) {
				return s < 10 ? '0' + s : s;
			},
			// 下载
			download(file){
				window.open(`${file}`)
			},
			// 初始化
			init(type) {
				this.type = type;
				if(type=='cross'){
					var obj = JSON.parse(localStorage.getItem('crossObj'));
					for (var o in obj){
						if(o=='qichemingcheng'){
							this.ruleForm.qichemingcheng = obj[o];
							this.ro.qichemingcheng = true;
							continue;
						}
						if(o=='qichetupian'){
							this.ruleForm.qichetupian = obj[o]?obj[o].split(",")[0]:'';
							this.ro.qichetupian = true;
							continue;
						}
						if(o=='qichepinpai'){
							this.ruleForm.qichepinpai = obj[o];
							this.ro.qichepinpai = true;
							continue;
						}
						if(o=='qicheleixing'){
							this.ruleForm.qicheleixing = obj[o];
							this.ro.qicheleixing = true;
							continue;
						}
						if(o=='shoujia'){
							this.ruleForm.shoujia = obj[o];
							this.ro.shoujia = true;
							continue;
						}
						if(o=='kucun'){
							this.ruleForm.kucun = obj[o];
							this.ro.kucun = true;
							continue;
						}
						if(o=='tianchuang'){
							this.ruleForm.tianchuang = obj[o];
							this.ro.tianchuang = true;
							continue;
						}
						if(o=='zuowei'){
							this.ruleForm.zuowei = obj[o];
							this.ro.zuowei = true;
							continue;
						}
						if(o=='qichepailiang'){
							this.ruleForm.qichepailiang = obj[o];
							this.ro.qichepailiang = true;
							continue;
						}
						if(o=='shangshinianfen'){
							this.ruleForm.shangshinianfen = obj[o];
							this.ro.shangshinianfen = true;
							continue;
						}
						if(o=='qichexiangqing'){
							this.ruleForm.qichexiangqing = obj[o];
							this.ro.qichexiangqing = true;
							continue;
						}
						if(o=='clicktime'){
							this.ruleForm.clicktime = obj[o];
							this.ro.clicktime = true;
							continue;
						}
						if(o=='clicknum'){
							this.ruleForm.clicknum = obj[o];
							this.ro.clicknum = true;
							continue;
						}
						if(o=='discussnum'){
							this.ruleForm.discussnum = obj[o];
							this.ro.discussnum = true;
							continue;
						}
						if(o=='storeupnum'){
							this.ruleForm.storeupnum = obj[o];
							this.ro.storeupnum = true;
							continue;
						}
					}
				}else if(type=='edit'){
					this.info()
				}
				// 获取用户信息
				this.$http.get(this.userTableName + '/session', {emulateJSON: true}).then(res => {
					if (res.data.code == 0) {
						var json = res.data.data;
					}
				});
				this.$http.get('option/qichepinpai/qichepinpai', {emulateJSON: true}).then(res => {
					if (res.data.code == 0) {
						this.qichepinpaiOptions = res.data.data;
					}
				});
				this.$http.get('option/qicheleixing/qicheleixing', {emulateJSON: true}).then(res => {
					if (res.data.code == 0) {
						this.qicheleixingOptions = res.data.data;
					}
				});
				this.tianchuangOptions = "有天窗,没天窗".split(',')
				this.zuoweiOptions = "2座,4座,5座,7座,其他".split(',')

				if (localStorage.getItem('raffleType') && localStorage.getItem('raffleType') != null) {
					localStorage.removeItem('raffleType')
					setTimeout(() => {
						this.onSubmit()
					}, 300)
				}
			},

			// 多级联动参数
			// 多级联动参数
			info() {
				this.$http.get(`qichexuangou/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
					if (res.data.code == 0) {
						this.ruleForm = res.data.data;
					}
				});
			},
			// 提交
			async onSubmit() {
				if(!this.ruleForm.id) {
					delete this.ruleForm.userid
				}
				await this.$refs["ruleForm"].validate(async valid => {
					if(valid) {
						if(this.type=='cross'){
							var statusColumnName = localStorage.getItem('statusColumnName');
							var statusColumnValue = localStorage.getItem('statusColumnValue');
							if(statusColumnName && statusColumnName!='') {
								var obj = JSON.parse(localStorage.getItem('crossObj'));
								if(!statusColumnName.startsWith("[")) {
									for (var o in obj){
										if(o==statusColumnName){
											obj[o] = statusColumnValue;
										}
									}
									var table = localStorage.getItem('crossTable');
									await this.$http.post(table+'/update', obj).then(res => {});
								}
							}
						}


						await this.$http.post(`qichexuangou/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
							if (res.data.code == 0) {
								this.$message({
									message: '操作成功',
									type: 'success',
									duration: 1500,
									onClose: () => {
										this.$router.go(-1);
										
									}
								});
							} else {
								this.$message({
									message: res.data.msg,
									type: 'error',
									duration: 1500
								});
							}
						});
					}
				});
			},
			// 获取uuid
			getUUID () {
				return new Date().getTime();
			},
			// 返回
			back() {
				this.$router.go(-1);
			},
			qichetupianUploadChange(fileUrls) {
				this.ruleForm.qichetupian = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
		}
	};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.add-update-preview {
		padding: 20px 16%;
		margin: 10px auto;
		background: #fff;
		width: 100%;
		position: relative;
		.add-update-form {
			border: 1px solid #BBB09B;
			border-radius: 50px;
			padding: 30px;
			width: 100%;
			position: relative;
			.add-item.el-form-item {
				padding: 10px;
				margin: 0 0 10px;
				background: none;
				display: inline-block;
				width: 49%;
				/deep/ .el-form-item__label {
					padding: 0 10px 0 0;
					margin: 0;
					color: #666;
					font-weight: 500;
					width: 90px;
					font-size: 13px;
					line-height: 50px;
					text-align: right;
				}
				/deep/ .el-form-item__content {
					margin-left: 90px;
				}
				.el-input {
					width: 100%;
				}
				.el-input /deep/ .el-input__inner {
					border: 1px solid #BBB09B;
					border-radius: 10px;
					padding: 0 12px;
					box-shadow: 0 0 0px rgba(64, 158, 255, .5);
					outline: none;
					color: #000;
					width: 100%;
					font-size: 15px;
					line-height: 50px;
					height: 50px;
				}
				.el-input /deep/ .el-input__inner[readonly="readonly"] {
					border: 1px solid #BBB09B;
					cursor: not-allowed;
					border-radius: 10px;
					padding: 0 12px;
					box-shadow: 0 0 0px rgba(85, 85, 127, 0.5);
					outline: none;
					color: #000;
					background: #eee;
					width: 100%;
					font-size: 15px;
					height: 50px;
				}
				.el-input-number /deep/ .el-input__inner {
					text-align: left;
					border: 1px solid #BBB09B;
					border-radius: 10px;
					padding: 0 12px;
					box-shadow: 0 0 0px rgba(64, 158, 255, .5);
					outline: none;
					color: #000;
					width: 100%;
					font-size: 15px;
					line-height: 50px;
					height: 50px;
				}
				.el-input-number /deep/ .is-disabled .el-input__inner {
					text-align: left;
					border: 1px solid #BBB09B;
					cursor: not-allowed;
					border-radius: 10px;
					padding: 0 12px;
					box-shadow: 0 0 0px rgba(85, 85, 127, 0.5);
					outline: none;
					color: #000;
					background: #eee;
					width: 100%;
					font-size: 15px;
					height: 50px;
				}
				.el-input-number /deep/ .el-input-number__decrease {
					display: none;
				}
				.el-input-number /deep/ .el-input-number__increase {
					display: none;
				}
				.el-select {
					width: 100%;
				}
				.el-select /deep/ .el-input__inner {
					border: 1px solid #BBB09B;
					border-radius: 10px;
					padding: 0 10px;
					box-shadow: 0 0 0px rgba(64, 158, 255, .5);
					outline: none;
					color: #000;
					width: 100%;
					font-size: 15px;
					height: 50px;
				}
				.el-select /deep/ .is-disabled .el-input__inner {
					border: 1px solid #BBB09B;
					cursor: not-allowed;
					border-radius: 10px;
					padding: 0 10px;
					box-shadow: 0 0 0px rgba(85, 85, 127, 0.5);
					outline: none;
					color: #000;
					background: #eee;
					width: 100%;
					font-size: 15px;
					height: 50px;
				}
				.el-date-editor {
					width: 100%;
				}
				.el-date-editor /deep/ .el-input__inner {
					border: 1px solid #BBB09B;
					border-radius: 10px;
					padding: 0 10px 0 30px;
					box-shadow: 0 0 0px rgba(64, 158, 255, .5);
					outline: none;
					color: #000;
					width: 100%;
					font-size: 15px;
					height: 50px;
				}
				.el-date-editor /deep/ .el-input__inner[readonly="readonly"] {
					border: 1px solid #BBB09B;
					cursor: not-allowed;
					border-radius: 10px;
					padding: 0 10px 0 30px;
					box-shadow: 0 0 0px rgba(85, 85, 127, 0.5);
					outline: none;
					color: #000;
					background: #eee;
					width: 100%;
					font-size: 15px;
					height: 50px;
				}
				/deep/ .el-upload--picture-card {
					background: transparent;
					border: 0;
					border-radius: 0;
					width: auto;
					height: auto;
					line-height: initial;
					vertical-align: middle;
				}
				/deep/ .upload .upload-img {
					border: 1px solid #BBB09B;
					cursor: pointer;
					border-radius: 6px;
					color: #000;
					width: 150px;
					font-size: 32px;
					line-height: 60px;
					text-align: center;
					height: 60px;
				}
				/deep/ .el-upload-list .el-upload-list__item {
					border: 1px solid #BBB09B;
					cursor: pointer;
					border-radius: 6px;
					color: #000;
					width: 150px;
					font-size: 32px;
					line-height: 60px;
					text-align: center;
					height: 60px;
					font-size: 14px;
					line-height: 1.8;
				}
				/deep/ .el-upload .el-icon-plus {
					border: 1px solid #BBB09B;
					cursor: pointer;
					border-radius: 6px;
					color: #000;
					width: 150px;
					font-size: 32px;
					line-height: 60px;
					text-align: center;
					height: 60px;
				}
				/deep/ .el-upload__tip {
					color: #BBB09B;
					line-height: 1;
				}
				.el-textarea /deep/ .el-textarea__inner {
					border: 1px solid #BBB09B;
					border-radius: 10px;
					padding: 12px;
					box-shadow: 0 0 0px rgba(64, 158, 255, .5);
					outline: none;
					color: #000;
					width: 100%;
					font-size: 14px;
					height: 120px;
				}
				.el-textarea /deep/ .el-textarea__inner[readonly="readonly"] {
					border: 1px solid #BBB09B;
					cursor: not-allowed;
					border-radius: 10px;
					padding: 12px;
					box-shadow: 0 0 0px rgba(64, 158, 255, .5);
					outline: none;
					color: #000;
					background: #eee;
					width: 100%;
					font-size: 14px;
					height: 120px;
				}
				/deep/ .el-input__inner::placeholder {
					color: #999;
					font-size: 15px;
				}
				/deep/ textarea::placeholder {
					color: #999;
					font-size: 15px;
				}
				.editor {
					background-color: #fff;
					border-radius: 0;
					padding: 0;
					box-shadow: 0 0 0px rgba(75,223,201,.5);
					margin: 0;
					width: 100%;
					border-color: #ccc;
					border-width: 0;
					border-style: solid;
					height: auto;
				}
				.upload-img {
					width: 100px;
					height: 100px;
				}
				.viewBtn {
					border: 0;
					cursor: pointer;
					padding: 0 10px;
					margin: 0;
					color: #fff;
					display: inline-block;
					font-size: 14px;
					line-height: 30px;
					border-radius: 0;
					outline: none;
					background: #BBB09B;
					width: auto;
					height: 30px;
				}
				.viewBtn:hover {
					background: #BBB09B90;
				}
				.unviewBtn {
					border: 0;
					cursor: not-allowed;
					padding: 0 10px;
					margin: 0;
					color: #fff;
					display: inline-block;
					font-size: 14px;
					line-height: 30px;
					border-radius: 0;
					outline: none;
					background: #AAA190;
					width: auto;
					height: 30px;
				}
				.unviewBtn:hover {
					background: #AAA190;
				}
			}
			.add-btn-item {
				padding: 0;
				margin: 0;
				text-align: center;
				.submitBtn {
					border: 0;
					cursor: pointer;
					border-radius: 0;
					padding: 0 35px;
					margin: 0 20px 0 0;
					outline: none;
					background: #BBB09B;
					display: inline-block;
					width: auto;
					font-size: 14px;
					line-height: 50px;
					height: 50px;
					.icon {
						color: rgba(255, 255, 255, 1);
						display: none;
					}
					.text {
						color: rgba(255, 255, 255, 1);
					}
				}
				.submitBtn:hover {
					opacity: 0.5;
					.icon {
						color: #000;
					}
					.text {
						color: #fff;
					}
				}
				.closeBtn {
					border: 0;
					cursor: pointer;
					border-radius: 0;
					padding: 0 35px;
					margin: 0 20px 0 0;
					outline: none;
					background: #BBB09B;
					display: inline-block;
					width: auto;
					font-size: 14px;
					line-height: 50px;
					height: 50px;
					.icon {
						color: rgba(64, 158, 255, 1);
						display: none;
					}
					.text {
						color: #fff;
					}
				}
				.closeBtn:hover {
					opacity: 0.5;
					.icon {
						color: rgba(64, 158, 255, 0.5);
					}
					.text {
						color: #fff;
					}
				}
			}
		}
	}
	.el-date-editor.el-input {
		width: auto;
	}
</style>
