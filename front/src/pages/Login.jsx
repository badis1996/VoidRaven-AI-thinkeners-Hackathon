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


function Login() {
	let history = useHistory();
	const [error, setError] = useState(null);

	const [username, setUsername] = useState();
	const [password, setPassword] = useState();

	let data = {
		username: username,
        password: password
	};

	let req = { method: 'POST',
	    headers: { 'Content-Type': 'application/json' },
	    mode: 'cors',
	    cache: 'default',
	    body: JSON.stringify(data)
	};

	let url = new Request(getApiUrl() + "user/login");

	const handleLoginSubmit = async e => {
		setError(null);
		e.preventDefault();

		await fetch(url, req)
			.then(function(response) {
			  if (response.status !== 200) {
				setError("Username or password is incorrect, please try again.");
				return;
			  }

			  response.json().then(function(data) {
			    setUserSession(data.token, data.user.pseudo);
				history.push('/dashboard/');
			  });
			})
			.catch(function(err) {
				console.log('Fetch Error :-S', err);
				removeUserSession();
				setError(err);
			});
	}

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
			<div className="auth-form">
				<div className="auth-form-header">
					<h1 className="form-title signin-title">
						Login to Dashboard
					</h1>
					{error
						? <p className="auth-form-error"><FontAwesomeIcon icon={faTriangleExclamation} />&nbsp;&nbsp;{error}</p>
						: <p className="auth-form-error-empty"></p>
					}
				</div>
				<form onSubmit={handleLoginSubmit}>
					<p className="auth-form-label">
						<b>Email address or Username</b>
					</p>
					<input  type="email" 
							name="email"
							placeholder="Your email address or username"
							className="auth-form-input"
							required 
							autoFocus />
					<p className="auth-form-label">
						<b>Password</b>
					</p>
					<div className="user-box">
						<input  type="password"
								id="input-pwd"
								name="password"
								placeholder="Your password"
								className="auth-form-input"
								autoComplete="off"
								required />
					</div>
					<input  type="submit" 
							value="Get Started"
							className="auth-form-btn" />
				</form>
			</div>
		</div>
	);
}

export default memo(Login);