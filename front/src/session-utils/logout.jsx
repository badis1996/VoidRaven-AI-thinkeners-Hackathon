import React from 'react';
import { useHistory } from "react-router-dom";
import { Button } from 'react-bootstrap';
import { removeUserSession } from './UserSession';
import { faSignOutAlt } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import './../assets/css/style.css';

function Logout(props) {
  const history = useHistory();
  const { collapsed } = props;

  const handleLogout = () =>{ 
    removeUserSession();
    history.push('/');
  }

  return (
      <>	      
        {!collapsed
          ? <Button variant="outline-danger"
              onClick={handleLogout}
              title="Logout">
                <FontAwesomeIcon icon={faSignOutAlt} /> 
            </Button>
          : <button className="btn-as-link-red" 
                    onClick={handleLogout} >
              Logout &nbsp;&nbsp;<FontAwesomeIcon icon={faSignOutAlt} />
            </button>
        }
      </>
  );
}

export default Logout;