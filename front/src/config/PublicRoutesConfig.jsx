import {
	Homepage,
    Login,
	Interview,
	PublicDashboard,
} from '../pages';

const PublicRoutesConfig = [
	{
		component: Homepage,
		path: '/',
		title: 'Home',
		tabTitle: 'Home',
		permission: [
		]
	},
	{
		component: Interview,
		path: 'interview',
		title: 'Interview',
		tabTitle: 'Interview',
		permission: [
		]
	},
	{
		component: Login,
		path: 'login',
		title: 'Login',
		tabTitle: 'Login',
		permission: [
		]
	},
	{
		component: PublicDashboard,
		path: 'dashboard',
		title: 'Public Dashboard',
		tabTitle: 'Public Dashboard',
		permission: [
	]
	},
];

export default PublicRoutesConfig;