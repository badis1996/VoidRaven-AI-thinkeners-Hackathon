import React, { memo } from 'react';
import { isLoggedIn } from '../session-utils';
import PublicRoutes from './PublicRoutes';
import PrivateRoutes from './PrivateRoutes';


function Auth() {
	return isLoggedIn() ? (
			<PrivateRoutes />
		) : (
			<PublicRoutes />
		)
}

export default memo(Auth);
