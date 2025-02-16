import React, { memo } from 'react';
import { Router, Route, Switch } from 'react-router-dom';
import history from './../session-utils/history';
import Auth from './Auth';
import PublicRoutes from './PublicRoutes';
import ScrollToTop from './ScrollToTop';


function AppRoutes() {
	return (
		<Router history={history}>
			<ScrollToTop />
			<Switch>
				<Route path="/dashboard">
					<Auth />
				</Route>
				<Route path="/">
					<PublicRoutes />
				</Route>
			</Switch>
		</Router>
	)
}

export default memo(AppRoutes);

