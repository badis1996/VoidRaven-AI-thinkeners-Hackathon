export const getApiUrl = () => {
	if (process.env.REACT_APP_IN_PRODUCTION === "TRUE")
		return process.env.REACT_APP_PROD_API_KEY + "api/";
	else
		return process.env.REACT_APP_LOCAL_API_KEY + "api/";
}

export const getRessouresUrl = () => {
	if (process.env.REACT_APP_IN_PRODUCTION === "TRUE") 
		return process.env.REACT_APP_PROD_API_KEY;
	else
		return process.env.REACT_APP_LOCAL_API_KEY;
}