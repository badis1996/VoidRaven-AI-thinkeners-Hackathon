import React, { Component, memo } from "react";
import CircularLoading from "../components/circular-loading/CircularLoading";
import Vapi from "@vapi-ai/web";

import './../assets/css/style.css'


class Interview extends Component {
    constructor(props) {
      super(props);
      this.state = {
        assitant: [],
        isLoaded: false,
        vapi: new Vapi(process.env.VAPI_BEARER_TOKEN)
      }
    }
  
    componentDidMount() {
        // fetch("https://api.vapi.ai/assistant/" + process.env.VAPI_ASSITANT_ID, {
        //     method: 'GET',
        //     headers: {
        //         'Content-Type': 'application/json',
        //         'Authorization': 'Bearer ' + process.env.VAPI_BEARER_TOKEN
        //     },
        //     // mode: 'cors',
        //     // cache: 'default',
        //     // credentials: 'omit'
        // })
        // .then(data => data.json())
        // .then(data => this.setState({ 
        //     isLoaded: true, 
        //     assitant: data
        //  }))
        // .catch(error => console.log(error))

        // const call = await vapi.start(assistantId);
    }

    render() {
        if (!this.state.isLoaded) {
            return <div><CircularLoading /></div>;
        } else if (!this.state.assitant) {
            return <p>No response</p>;
        } else {
            return (  <>
                    {this.state.assitant.message}
                    </>);
        }
    }
}

export default memo(Interview);