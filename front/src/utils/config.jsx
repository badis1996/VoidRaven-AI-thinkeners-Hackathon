export const getApiUrl = () => {
	if (process.env.REACT_APP_IN_PRODUCTION === "TRUE")
		return "https://safe-elise-logispear-d8964e07.koyeb.app/";
	else
		return "http://localhost:8000/";
}

export const getRessouresUrl = () => {
	if (process.env.REACT_APP_IN_PRODUCTION === "TRUE") 
		return process.env.REACT_APP_PROD_API_KEY;
	else
		return process.env.REACT_APP_LOCAL_API_KEY;
}