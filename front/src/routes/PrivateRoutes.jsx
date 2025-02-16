import React, { Fragment } from 'react';
import { Redirect, useRouteMatch } from 'react-router-dom';
import { getVisibleRoutes, getAllowedRoutes, isLoggedIn } from '../session-utils';
import { PrivateRoutesConfig } from '../config';
// import Header from '../components/navbar';
import MapAllowedRoutes from './MapAllowedRoutes';
import ScrollToTopHelperButton from './ScrollToTopHelperButton';

function PrivateRoutes() {
	const match = useRouteMatch('/dashboard/');
	let allowedRoutes = [];
	let visibleRoutes = [];

	if (isLoggedIn()) allowedRoutes = getAllowedRoutes(PrivateRoutesConfig);
	if (isLoggedIn()) visibleRoutes = getVisibleRoutes(PrivateRoutesConfig);
	else return <Redirect to="/" />;

	return (
		<>
			<Fragment>
				<div className="wrapper">
					{/* <Header routes={visibleRoutes} prefix={match.path} /> */}
					<div className="content">
						<MapAllowedRoutes routes={allowedRoutes} basePath="/dashboard/" isAddNotFound />
						<ScrollToTopHelperButton />
					</div>
				</div>
			</Fragment>
		</>
	);
}

export default PrivateRoutes;
