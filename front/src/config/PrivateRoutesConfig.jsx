import { Roles } from '.'
import {
	Dashboard,
	CandidateView,
} from '../pages';

const PrivateRoutesConfig = [
	{
		component: Dashboard,
		path: '/',
		title: 'Dashboard',
		tabTitle: 'Dashboard',
		permission: [
			Roles.ADMINISTRATION
		]
	},
	{
		component: CandidateView,
		path: 'candidate-view',
		title: 'Candidate View',
		tabTitle: 'Candidate View',
		permission: [
			Roles.ADMINISTRATION
		]
	},
];

export default PrivateRoutesConfig;