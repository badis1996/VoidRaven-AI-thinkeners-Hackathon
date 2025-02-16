import { Roles } from '../config';

// return the token from the session storage
export const getToken = () => {
  return sessionStorage.getItem('token') || null;
}

// return the user pseudo from the session storage
export const getUser = () => {
  const userStr = sessionStorage.getItem('user');
  if (userStr) return JSON.parse(userStr);
  else return null;
}

// return the role from the session storage
export const getRole = () => {
  const roleStr = sessionStorage.getItem('role');
  if (roleStr) return JSON.parse(roleStr);
  else return null;
}

// remove the token and user from the session storage
export const removeUserSession = () => {
  sessionStorage.removeItem('token');
  sessionStorage.removeItem('user');
  sessionStorage.removeItem('role');
}
 
// set the token and user from the user session storage
export const setUserSession = (token, user) => {
  sessionStorage.setItem('token', token);
  sessionStorage.setItem('user', JSON.stringify(user));
  sessionStorage.setItem('role', JSON.stringify(Roles.ADMINISTRATION));
} 
