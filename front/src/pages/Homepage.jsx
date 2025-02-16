import React, { memo, useState } from 'react';
import { useHistory } from "react-router-dom";
// import { JumbotronWrapper } from '../components/common';
import { getApiUrl } from '../utils/config';
import { setUserSession, removeUserSession } from '../session-utils/UserSession';

import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons";

import "./../assets/css/style.css";
import "./../assets/css/login.css";


function Homepage() {
	let history = useHistory();
	const [error, setError] = useState(null);

	const [fullname, setFullname] = useState();
	const [email, setEmail] = useState();
	const [cv, setCV] = useState();

	const handleLoginSubmit = async e => {
		setError(null);
		e.preventDefault();

		const formData = new FormData();
		formData.append('name', fullname);
		formData.append('email', email);
		formData.append('cv_file', cv);

		try {
			const response = await fetch(getApiUrl() + "api/v1/candidates", {
				method: 'POST',
				mode: 'cors',
				body: formData
			});
			
			if (response.status !== 201) {
				setError("Something went wrong, please try again.");
				return;
			}

			const data = await response.json();
			//setUserSession(data.token, data.user.pseudo);
			history.push('/interview');
			
		} catch (err) {
			console.log('Fetch Error :-S', err);
			removeUserSession();
			setError("Network error occurred. Please try again later.");
		}
	}

	const handleFileChange = (e) => {
		if (e.target.files) {
			setCV(e.target.files[0]);
		}
	};

	return (
	    // <JumbotronWrapper title="Login" className="text-center">
		// 	<hr />
	    // 	{error && <><small style={{ color: 'red' }}>{error}</small><br /></>}<br />
	    //     <form onSubmit={handleLoginSubmit}>
		// 		<div className="form-group">
		// 			<input type="text" className="form-control" id="username" placeholder="Username" onChange={e => setUsername(e.target.value.toLowerCase())} required autoFocus={true}/>
		// 		</div>
		// 		<div className="form-group">
		// 			<input type="password" className="form-control" id="password" placeholder="Password" onChange={e => setPassword(e.target.value)} required/>
		// 		</div>
		// 		<br />
		// 		<Button variant="warning"
		// 				type="submit"
		// 				style={{ width: "100%", height: "40px", borderRadius: "10px" }}>
		// 			Submit
		// 		</Button>
	    //     </form>
		// </JumbotronWrapper>

		<div className="center-to-screen">
			<div className="getting-started-form">
				<div className="auth-form-header">
					<h1 className="form-title signin-title">
                        Launch Your Interview Experience
					</h1>
                    <p className="signup-prompt">
                        Ready to begin? Just fill out the following information and dive into your interview – it's quick and easy!
                    </p>
					{error
						? <p className="auth-form-error"><FontAwesomeIcon icon={faTriangleExclamation} />&nbsp;&nbsp;{error}</p>
						: <p className="auth-form-error-empty"></p>
					}
				</div>
				<form onSubmit={handleLoginSubmit}>
					<p className="auth-form-label">
						<b>Full Name</b>
					</p>
					<input  type="text" 
							name="text"
							placeholder="John Doe"
							className="auth-form-input"
                            onChange={e => setFullname(e.target.value)} 
							required 
							autoFocus />
					<p className="auth-form-label">
						<b>Email address</b>
					</p>
					<input  type="email" 
							name="email"
							placeholder="john.doe@mail.com"
							className="auth-form-input"
                            onChange={e => setEmail(e.target.value)} 
							required />
                    <p className="auth-form-label">
						<b>Curriculum vitæ (CV)</b>
					</p>
					<input  type="file" 
							name="cv"
							className="auth-form-input"
							onChange={handleFileChange}
							required />
					<input  type="submit" 
							value="Get Started"
							className="auth-form-btn" />
				</form>
                <div className="form-notice signin-notice">
                    <span>
                        Not your device? Use a private window.
                        <br />
                        See our <Link className="notice" to='/privacy'>Privacy Policy</Link> for more info.
                    </span>
                </div>
			</div>
		</div>
	);
}

export default memo(Homepage);