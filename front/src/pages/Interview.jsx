import React, { Component, memo } from "react";
import { useLocation } from "react-router-dom";
import CircularLoading from "../components/circular-loading/CircularLoading";
import { getApiUrl } from '../utils/config';
import Vapi from "@vapi-ai/web";
import Webcam from "react-webcam";

import './../assets/css/style.css';
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";


const Interview = props => {
    const location = useLocation();
    const history = useHistory();
    return <InterviewMain location={location} history={history} {...props} /> // your component
} 

class InterviewMain extends Component {
    constructor(props) {
      super(props);
      this.state = {
        assitant: [],
        isLoaded: false,
        vapi: null,
        error: null,
      }
    }
  
    async componentDidMount() {
        const vapi = new Vapi("28d63dce-0ba1-4ee1-a228-7706408affea");

        const content = "You are an AI admissions interviewer for Paris Business School. Your task is to conduct an interview with a candidate based on their CV and the school's information. Follow these instructions carefully:\n\n1. First, review the candidate's CV:\n"+this.props.location.state.cv_data+"\n\n2. Next, familiarize yourself with the school information:\nParis Business School\n\n\n3. Persona Definition:\nYour name is Brian, and you are a senior admissions interviewer at Paris Business School. Embody the following traits:\n- Professional and courteous\n- Insightful and perceptive\n- Encouraging but objective\n- Detail-oriented\n- Knowledgeable about Paris Business School's programs and values\n\n4. Interview Preparation:\n- Analyze the CV for key points related to academic background, work experience, extracurricular activities, and achievements.\n- Prepare a list of at least 5 tailored questions based on the candidate's profile and how it aligns with Paris Business School's programs and values.\n- Plan to assess the candidate's motivation, leadership potential, and cultural fit.\n\n5. Conducting the Interview:\n- Begin with a warm welcome and a brief introduction of yourself and Paris Business School.\n- Structure the interview as follows:\n a. Warm-up questions to put the candidate at ease\n b. Questions about academic background and achievements\n c. Inquiries about work experience and extracurricular activities\n d. Probing questions about motivation for pursuing an MBA at Paris Business School\n e. Scenarios or questions to assess leadership potential\n f. Questions to evaluate cultural fit and international perspective\n g. Opportunity for the candidate to ask questions\n h. Closing statements\n\n- Adapt your questions based on the candidate's responses. If they mention something interesting or relevant, probe deeper.\n- Use your knowledge of Paris Business School to relate the candidate's experiences to the school's programs and values.\n\nRemember to maintain a professional and encouraging tone throughout the interview simulation. Your goal is to assess the candidate's suitability for Paris Business School while also representing the school in a positive light.\n\nAt the end of the interview you must thank the applicant of making the time and that the team will reach out back soon. You have to say goodbye at the end.";

        const call = await vapi.start("33f29c81-602e-4e7a-92d5-b5b29715d156");
        vapi.start(
            {
                "id": "33f29c81-602e-4e7a-92d5-b5b29715d156",
                "orgId": "bd8a9f21-42fc-4def-91b3-19b47a1ebe73",
                "name": "University submission AI interviewer",
                "voice": {
                    "model": "eleven_multilingual_v2",
                    "voiceId": "nPczCjzI2devNBz1zQrb",
                    "provider": "11labs",
                    "stability": 0.5,
                    "similarityBoost": 0.75
            },
            "createdAt": "2025-02-16T09:34:30.357Z",
            "updatedAt": "2025-02-16T12:18:06.352Z",
            "model": {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": content
                    }
                ],
                "provider": "openai",
                "temperature": 1,
                "knowledgeBaseId": "a6be97c0-7944-40d0-a0ed-c5656283301d"
            },
            "firstMessage": "Hi there, I am Brian and I will be your interviewer today, are you ready?",
            "endCallMessage": "goodbye",
            "transcriber": {
                "model": "nova-3",
                "language": "en",
                "provider": "deepgram"
            },
            "silenceTimeoutSeconds": 70,
            "clientMessages": [
                "transcript",
                "hang",
                "function-call",
                "speech-update",
                "metadata",
                "transfer-update",
                "conversation-update"
            ],
            "serverMessages": [
                "end-of-call-report",
                "status-update",
                "hang",
                "function-call"
            ],
            "hipaaEnabled": false,
            "maxDurationSeconds": 468,
            "backchannelingEnabled": false,
            "backgroundDenoisingEnabled": false,
            "artifactPlan": {
                "videoRecordingEnabled": true
            },
            "startSpeakingPlan": {
                "transcriptionEndpointingPlan": {
                "onPunctuationSeconds": 0.5
            }
            },
            "stopSpeakingPlan": {
                "numWords": 3
            },
            "isServerUrlSecretSet": false
           });

        // vapi.start({
        //     transcriber: {
        //       provider: "deepgram",
        //       model: "nova-2",
        //       language: "en-US",
        //     },
        //     model: {
        //       provider: "openai",
        //       model: "gpt-3.5-turbo",
        //       messages: [
        //         {
        //           role: "system",
        //           content: "You are a helpful assistant.",
        //         },
        //       ],
        //     },
        //     voice: {
        //       provider: "playht",
        //       voiceId: "jennifer",
        //     },
        //     name: "My Inline Assistant",
        // });
        vapi.on("call-start", () => {
            console.log("Call has started.");
        });
          
        vapi.on("speech-start", () => {
            console.log("Assistant speech has started.");
        });
        
        console.log("CALL ID: " + call.id);
        console.log("Data name: "+ this.props.location.state.name);
        console.log("Data email: "+ this.props.location.state.email);
        console.log("Data cv: " + this.props.location.state.cv_data);
        console.log("content: " + content);

        vapi.on("call-end", () => {
            console.log("Call has ended.");
        });
        
        this.setState({ isLoaded: true });
        this.setState({ call_id: call.id });
    }

    handleEndCall = async () => {
        this.setState({ error: null, isLoaded: false });

        try {
            const response = await fetch(getApiUrl() + "api/v1/candidates/vapi-transcript", {
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    call_id: this.state.call_id,
                    email: this.props.location.state.email
                })
            });

            
            this.setState({ isLoaded: true });

            this.props.history.push(
                {
                    pathname: '/dashboard', 
                    state: {
                        
                    }
                }
            );
            
        } catch (err) {
            console.log('Fetch Error :-S', err);
            this.setState("Network error occurred. Please try again later.");
            this.setState({ isLoaded: false });
        }
    }
    
    render() {
        if (!this.state.isLoaded) {
            return <div><CircularLoading /></div>;
        } else {
            return (
                <div className="center-to-screen">
                    <Webcam audio={false}
                            height={720}
                            screenshotFormat="image/jpeg"
                            width={1280} />

                    <form onSubmit={this.handleEndCall}>
                        { this.state.isLoaded && 
                            <input  type="submit" 
                                value="End Interview"
                                className="auth-form-btn-end-call"
                                style={{ position: 'relative' }} />
                        }
                    </form>

                </div>
            );
        }
    }
}

export default memo(Interview);