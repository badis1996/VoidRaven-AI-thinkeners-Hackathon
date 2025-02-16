import { useEffect } from 'react';
import { withRouter } from 'react-router-dom';

// This function resets (automatically) page scroll positioning to (0, 0) on each route change 
function ScrollToTop({ history }) {
  useEffect(() => {
    const unlisten = history.listen(() => {
      window.scrollTo(0, 0);
    });
    return () => {
      unlisten();
    }
  }, [history]);

  return (null);
}

export default withRouter(ScrollToTop);