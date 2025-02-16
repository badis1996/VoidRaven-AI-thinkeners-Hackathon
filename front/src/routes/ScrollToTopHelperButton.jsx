import React, { useState, useEffect } from 'react';
import { faArrowUp } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import './../assets/css/style.css';

// This component resets (on demand) page scroll positioning to (0, 0) on click event 
const ScrollToTopHelperButton = () => {
  // State to track whether the button should be visible
  const [isVisible, setIsVisible] = useState(false);

  // Effect to handle scroll events
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 500) {
        setIsVisible(true);  // Show button when scrolled more than 500px
      } else {
        setIsVisible(false); // Hide button when scrolled back to top
      }
    };

    // Adding event listener for scroll
    window.addEventListener('scroll', handleScroll);

    // Cleanup the event listener on component unmount
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  // Function to scroll to the top
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div>
      {/* Scroll to top button */}
      {isVisible && (
        <button
          onClick={scrollToTop}
          className="scroll-to-top-helper-button"
          title="Navigate to page top"
        >
          <FontAwesomeIcon icon={faArrowUp} />
        </button>
      )}
    </div>
  );
};

export default ScrollToTopHelperButton;