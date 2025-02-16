import React, { memo, useState, useEffect } from "react";
import { useParams } from "react-router-dom";

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
    <ul className="space-y-3">
      {items?.map((item, index) => (
        <li 
          key={index} 
          className="flex items-start"
        >
          <span className="inline-block w-2 h-2 mt-2 mr-3 bg-gray-400 rounded-full"></span>
          <span className="text-gray-700">{item}</span>
        </li>
      ))}
    </ul>
  );

  if (loading) {
    return (
      <div className="p-6 text-center">
        <div className="animate-pulse">Loading interview data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 max-w-2xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h2 className="text-red-700 font-semibold mb-2">Error Loading Interview</h2>
          <p className="text-red-600">{error}</p>
          <p className="text-sm text-red-500 mt-2">
            Please try refreshing the page or contact support if the issue persists.
          </p>
        </div>
      </div>
    );
  }

  if (!interviewData) {
    return <div className="p-6 text-center">No interview data found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="p-6 max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-gray-800 text-center">
          Interview Analysis Dashboard
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Left Column - Transcript */}
          <div className="bg-white p-8 rounded-xl shadow-lg border border-gray-100">
            <h2 className="text-2xl font-semibold mb-6 text-gray-800 flex items-center">
              <span className="mr-2">📝</span>
              Interview Transcript
            </h2>
            <div className="whitespace-pre-wrap bg-gray-50 p-6 rounded-lg border border-gray-200 text-gray-700 leading-relaxed max-h-[600px] overflow-y-auto">
              {interviewData.transcript}
            </div>
          </div>

          {/* Right Column - Evaluation */}
          <div className="space-y-6">
            {/* Summary */}
            <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 transition-all hover:shadow-xl">
              <h2 className="text-2xl font-semibold mb-4 text-gray-800 flex items-center">
                <span className="mr-2">📊</span>
                Summary
              </h2>
              <p className="text-gray-700 leading-relaxed">{interviewData.evaluation.summary}</p>
            </div>

            {/* Strengths */}
            <div className="bg-white p-6 rounded-xl shadow-lg border border-green-100 transition-all hover:shadow-xl">
              <h2 className="text-2xl font-semibold mb-4 text-green-600 flex items-center">
                <span className="mr-2">💪</span>
                Strengths
              </h2>
              {renderList(interviewData.evaluation.strengths)}
            </div>

            {/* Weaknesses */}
            <div className="bg-white p-6 rounded-xl shadow-lg border border-red-100 transition-all hover:shadow-xl">
              <h2 className="text-2xl font-semibold mb-4 text-red-600 flex items-center">
                <span className="mr-2">🔍</span>
                Areas for Improvement
              </h2>
              {renderList(interviewData.evaluation.weaknesses)}
            </div>

            {/* Feedback */}
            <div className="bg-white p-6 rounded-xl shadow-lg border border-blue-100 transition-all hover:shadow-xl">
              <h2 className="text-2xl font-semibold mb-4 text-blue-600 flex items-center">
                <span className="mr-2">💡</span>
                Feedback
              </h2>
              {renderList(interviewData.evaluation.feedback)}
            </div>

            {/* Topics to Discuss */}
            <div className="bg-white p-6 rounded-xl shadow-lg border border-purple-100 transition-all hover:shadow-xl">
              <h2 className="text-2xl font-semibold mb-4 text-purple-600 flex items-center">
                <span className="mr-2">🎯</span>
                Topics to Discuss
              </h2>
              {renderList(interviewData.evaluation.topicsToDiscuss)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default memo(PublicDashboard);