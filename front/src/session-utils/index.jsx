import { intersection } from 'lodash';
import { getToken, getRole } from './UserSession';

export function isLoggedIn() {
	// TODO 
	return !!getToken();
}

export function isArrayWithLength(arr) {
	return (Array.isArray(arr) && arr.length)
}

export function getAllowedRoutes(routes) {
	const role = getRole();
	return routes.filter(({ permission }) => {
		if(!permission) return true;
		else if(!isArrayWithLength(permission)) return true;
		else if(permission[0] === role) return true;
		else return intersection(permission, role).length;
	});
}

export function getVisibleRoutes(routes) {
	const role = getRole();
	return routes.filter(({ path, permission }) => {
		if(!permission) return true;
		else if(path === 'login' || path === '/') return false;
		else if(!isArrayWithLength(permission)) return true;
		else if(permission[0] === role) return true;
		else return intersection(permission, role).length;
	});
}
