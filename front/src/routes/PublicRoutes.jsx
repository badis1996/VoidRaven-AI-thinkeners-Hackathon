import React, { Fragment } from 'react';
import { useLocation } from 'react-router-dom';
import { getVisibleRoutes, getAllowedRoutes } from '../session-utils';
import { PublicRoutesConfig } from '../config';
// import Header from '../components/navbar';
// import Footer from '../components/footer/index';
import MapAllowedRoutes from './MapAllowedRoutes';
import ScrollToTopHelperButton from './ScrollToTopHelperButton';
import CircularLoading from './../components/circular-loading/CircularLoading';

import '../assets/css/style.css';

function PublicRoutes() {
	const match = useLocation();
	let allowedRoutes = getAllowedRoutes(PublicRoutesConfig);
	let visibleRoutes = getVisibleRoutes(PublicRoutesConfig);

	// console.log(match.pathname);

	// useEffect(() => {
	// 	const landingVideo = document.getElementById("landing-video");
	// 	if (landingVideo !== null) {
	// 		landingVideo.addEventListener('loadeddata', (e) => {
	// 			if (landingVideo.readyState >= 3) {
	// 				console.log("video loaded!");
	// 			}
	// 		})
	// 	}
	// });

	return (
		<>
			<Fragment>
				{/* {
					match.pathname === '/'
					? <CircularLoading />
					: null
				} */}

				<div className="wrapper">
					{/* <Header routes={visibleRoutes} prefix={match.path} /> */}
					<div className="content">
						<MapAllowedRoutes routes={allowedRoutes} basePath="/" isAddNotFound />
						<ScrollToTopHelperButton />
					</div>
					{/* <Footer /> */}
				</div>
			</Fragment>
		</>
	);
}

export default PublicRoutes;
