import React, { memo, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import './PublicDashboard.css';

function PublicDashboard() {
  const { id } = useParams();
  const [interviewData, setInterviewData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Mock data instead of fetching
    const mockData = {
      "transcript": "User: The user ID. On a\nAI: Hi there. I am Brian. I will be your interviewer today. Are you ready?\nUser: It's the 9 94 p Yes. Here's a caller ID from us.\nAI: It seems like your message got cut off or is incomplete. Could you please I'm here to help with any questions you may have. Especially regarding Paris Business School. You have specific inquiries about our programs, admission processes, or anything else, please feel free to ask.\nUser: I can I I yeah? I tried to do the evaluation part. I trained to get the the\nAI: It seems that your message might be incomplete or unclear. Could you please provide more context or clarify your question? I'm here to help with any specific queries you have regarding Paris Business School, or the admission process. Thank you.\nUser: Yeah. It's the same.\nAI: Thank you for your patience and for providing context throughout our conversation. If there's anything specific you'd like to discuss or any questions you have regarding the\nUser: Let's see.\nAI: Paris Business School, the application process please feel free to ask. I'm here to help.\nUser: I mean, no. I'm good.\nAI: In appears that your message might be incomplete. Thank you for letting me know. If you have any more questions in the future or need assistance, feel free to reach out. Have a great day. Goodbye. Thank you for your query. If there's anything specific you'd like to ask or discuss regarding Paris Business School, please feel free to share I'm here to assist you with any information you may need.\nUser: We just see\nAI: Thank you for your engagement. If you have any final questions or if there's anything specific you'd like to discuss regarding Paris Business School, please feel free to share. I'm here to help. It seems like your message got cut off. If you could please clarify your final query or provide more context, I would be more than happy to assist you. Thank you.\n",
      "evaluation": {
        "summary": "A highly fragmented and unclear conversation where the interviewer attempts to engage with a user who provides brief, incomplete responses. The context appears to be about Paris Business School, but the dialogue lacks coherence and direction.",
        "strengths": [
          "Interviewer maintains professional composure",
          "Consistent attempts to clarify and understand user's needs",
          "Polite and patient approach throughout",
          "Regular offers to provide assistance"
        ],
        "weaknesses": [
          "No clear communication established",
          "User responses are incomplete and unclear",
          "Conversation lacks structure and purpose",
          "Multiple instances of repetitive prompting",
          "No substantial information exchanged"
        ],
        "feedback": [
          "Consider establishing clear communication protocols at the start",
          "Implement a more structured approach to guide the conversation",
          "Use more direct questions to elicit clearer responses",
          "Consider technical issues that might be affecting communication"
        ],
        "topicsToDiscuss": [
          "Technical difficulties experienced during the interview",
          "User's actual needs and intentions",
          "Preferred communication method",
          "Specific areas of interest regarding Paris Business School"
        ]
      }
    };

    // Simulate loading
    setTimeout(() => {
      setInterviewData(mockData);
      setLoading(false);
    }, 500);
  }, [id]);

  const renderList = (items) => (
    <ul className="item-list">
      {items?.map((item, index) => (
        <li key={index} className="list-item">
          <span className="bullet"></span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-text">Loading interview data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-box">
          <h2 className="error-title">Error Loading Interview</h2>
          <p className="error-message">{error}</p>
          <p className="error-help">
            Please try refreshing the page or contact support if the issue persists.
          </p>
        </div>
      </div>
    );
  }

  if (!interviewData) {
    return <div className="no-data">No interview data found</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        <h1 className="dashboard-title">Interview Analysis Dashboard</h1>
        
        <div className="content-wrapper">
          {/* Left Column - Transcript */}
          <div className="transcript-section">
            <h2 className="section-title">
              <span className="icon">📝</span>
              Interview Transcript
            </h2>
            <div className="transcript-content">
              {interviewData.transcript}
            </div>
          </div>

          {/* Right Column - Evaluation */}
          <div className="evaluation-section">
            {/* Summary */}
            <div className="summary-box">
              <h2 className="section-title">
                <span className="icon">📊</span>
                Summary
              </h2>
              <p>{interviewData.evaluation.summary}</p>
            </div>

            <div className="evaluation-grid">
              {/* Strengths */}
              <div className="evaluation-box strengths">
                <h2 className="section-title">
                  <span className="icon">💪</span>
                  Strengths
                </h2>
                {renderList(interviewData.evaluation.strengths)}
              </div>

              {/* Weaknesses */}
              <div className="evaluation-box weaknesses">
                <h2 className="section-title">
                  <span className="icon">🔍</span>
                  Areas for Improvement
                </h2>
                {renderList(interviewData.evaluation.weaknesses)}
              </div>

              {/* Feedback */}
              <div className="evaluation-box feedback">
                <h2 className="section-title">
                  <span className="icon">💡</span>
                  Feedback
                </h2>
                {renderList(interviewData.evaluation.feedback)}
              </div>

              {/* Topics to Discuss */}
              <div className="evaluation-box topics">
                <h2 className="section-title">
                  <span className="icon">🎯</span>
                  Topics to Discuss
                </h2>
                {renderList(interviewData.evaluation.topicsToDiscuss)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default memo(PublicDashboard);