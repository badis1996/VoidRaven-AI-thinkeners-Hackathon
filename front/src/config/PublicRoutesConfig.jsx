import {
	Homepage,
    Login,
	Interview,
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
		path: '/login',
		title: 'Login',
		tabTitle: 'Login',
		permission: [
		]
	},
];

export default PublicRoutesConfig;