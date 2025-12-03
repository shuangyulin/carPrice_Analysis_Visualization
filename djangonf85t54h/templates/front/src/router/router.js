import VueRouter from 'vue-router'
//引入组件
import Index from '../pages'
import Home from '../pages/home/home'
import Login from '../pages/login/login'
import Register from '../pages/register/register'
import Center from '../pages/center/center'
import Storeup from '../pages/storeup/list'
import payList from '../pages/pay'

import yonghuList from '../pages/yonghu/list'
import yonghuDetail from '../pages/yonghu/detail'
import yonghuAdd from '../pages/yonghu/add'
import qichepinpaiList from '../pages/qichepinpai/list'
import qichepinpaiDetail from '../pages/qichepinpai/detail'
import qichepinpaiAdd from '../pages/qichepinpai/add'
import qicheleixingList from '../pages/qicheleixing/list'
import qicheleixingDetail from '../pages/qicheleixing/detail'
import qicheleixingAdd from '../pages/qicheleixing/add'
import qichexuangouList from '../pages/qichexuangou/list'
import qichexuangouDetail from '../pages/qichexuangou/detail'
import qichexuangouAdd from '../pages/qichexuangou/add'
import wodedinggouList from '../pages/wodedinggou/list'
import wodedinggouDetail from '../pages/wodedinggou/detail'
import wodedinggouAdd from '../pages/wodedinggou/add'
import tichexinxiList from '../pages/tichexinxi/list'
import tichexinxiDetail from '../pages/tichexinxi/detail'
import tichexinxiAdd from '../pages/tichexinxi/add'
import qichexinxiList from '../pages/qichexinxi/list'
import qichexinxiDetail from '../pages/qichexinxi/detail'
import qichexinxiAdd from '../pages/qichexinxi/add'
import qichexinxiforecastList from '../pages/qichexinxiforecast/list'
import qichexinxiforecastDetail from '../pages/qichexinxiforecast/detail'
import qichexinxiforecastAdd from '../pages/qichexinxiforecast/add'
import aboutusList from '../pages/aboutus/list'
import aboutusDetail from '../pages/aboutus/detail'
import aboutusAdd from '../pages/aboutus/add'
import systemintroList from '../pages/systemintro/list'
import systemintroDetail from '../pages/systemintro/detail'
import systemintroAdd from '../pages/systemintro/add'
import discussqichexuangouList from '../pages/discussqichexuangou/list'
import discussqichexuangouDetail from '../pages/discussqichexuangou/detail'
import discussqichexuangouAdd from '../pages/discussqichexuangou/add'
import discussqichexinxiList from '../pages/discussqichexinxi/list'
import discussqichexinxiDetail from '../pages/discussqichexinxi/detail'
import discussqichexinxiAdd from '../pages/discussqichexinxi/add'

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}

//配置路由
export default new VueRouter({
	routes:[
		{
      path: '/',
      redirect: '/index/home'
    },
		{
			path: '/index',
			component: Index,
			children:[
				{
					path: 'home',
					component: Home
				},
				{
					path: 'center',
					component: Center,
				},
				{
					path: 'pay',
					component: payList,
				},
				{
					path: 'storeup',
					component: Storeup
				},
				{
					path: 'yonghu',
					component: yonghuList
				},
				{
					path: 'yonghuDetail',
					component: yonghuDetail
				},
				{
					path: 'yonghuAdd',
					component: yonghuAdd
				},
				{
					path: 'qichepinpai',
					component: qichepinpaiList
				},
				{
					path: 'qichepinpaiDetail',
					component: qichepinpaiDetail
				},
				{
					path: 'qichepinpaiAdd',
					component: qichepinpaiAdd
				},
				{
					path: 'qicheleixing',
					component: qicheleixingList
				},
				{
					path: 'qicheleixingDetail',
					component: qicheleixingDetail
				},
				{
					path: 'qicheleixingAdd',
					component: qicheleixingAdd
				},
				{
					path: 'qichexuangou',
					component: qichexuangouList
				},
				{
					path: 'qichexuangouDetail',
					component: qichexuangouDetail
				},
				{
					path: 'qichexuangouAdd',
					component: qichexuangouAdd
				},
				{
					path: 'wodedinggou',
					component: wodedinggouList
				},
				{
					path: 'wodedinggouDetail',
					component: wodedinggouDetail
				},
				{
					path: 'wodedinggouAdd',
					component: wodedinggouAdd
				},
				{
					path: 'tichexinxi',
					component: tichexinxiList
				},
				{
					path: 'tichexinxiDetail',
					component: tichexinxiDetail
				},
				{
					path: 'tichexinxiAdd',
					component: tichexinxiAdd
				},
				{
					path: 'qichexinxi',
					component: qichexinxiList
				},
				{
					path: 'qichexinxiDetail',
					component: qichexinxiDetail
				},
				{
					path: 'qichexinxiAdd',
					component: qichexinxiAdd
				},
				{
					path: 'qichexinxiforecast',
					component: qichexinxiforecastList
				},
				{
					path: 'qichexinxiforecastDetail',
					component: qichexinxiforecastDetail
				},
				{
					path: 'qichexinxiforecastAdd',
					component: qichexinxiforecastAdd
				},
				{
					path: 'aboutus',
					component: aboutusList
				},
				{
					path: 'aboutusDetail',
					component: aboutusDetail
				},
				{
					path: 'aboutusAdd',
					component: aboutusAdd
				},
				{
					path: 'systemintro',
					component: systemintroList
				},
				{
					path: 'systemintroDetail',
					component: systemintroDetail
				},
				{
					path: 'systemintroAdd',
					component: systemintroAdd
				},
				{
					path: 'discussqichexuangou',
					component: discussqichexuangouList
				},
				{
					path: 'discussqichexuangouDetail',
					component: discussqichexuangouDetail
				},
				{
					path: 'discussqichexuangouAdd',
					component: discussqichexuangouAdd
				},
				{
					path: 'discussqichexinxi',
					component: discussqichexinxiList
				},
				{
					path: 'discussqichexinxiDetail',
					component: discussqichexinxiDetail
				},
				{
					path: 'discussqichexinxiAdd',
					component: discussqichexinxiAdd
				},
			]
		},
		{
			path: '/login',
			component: Login
		},
		{
			path: '/register',
			component: Register
		},
	]
})
