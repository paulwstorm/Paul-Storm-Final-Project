import React from 'react';
import { Component } from 'react'
import { Button, Card, Row, Col, Image } from 'react-bootstrap'
import './intro.css'



class IntroPosts extends Component {
    render() {
        return (
            <div className="intro">
                <h3 className="intro-header">Welcome to Posts!</h3>
                <p className="intro-paragraph">On this page you can see recent posts tailored to your reading level!</p>
                <p className="intro-paragraph">Use these buttons to toggle between reading posts and playing a fill-in-the-blank challenge:</p>
                <br/>
                <Image className="sample-post" src="https://raw.githubusercontent.com/paulwstorm/Paul-Storm-Final-Project/images/server/images/Screen%20Shot%202020-04-06%20at%207.45.45%20PM.png"></Image>
                <br/>
                <p className="intro-paragraph">
                    Click on any character in the post to see the definition
                </p>
                <br/>
                <p className="intro-paragraph">
                    Clicking the "+" on any post or dictionary entry allows you to save
                    the word or post for later study.
                </p>
                <Image className="add-word-pic" src="https://raw.githubusercontent.com/paulwstorm/Paul-Storm-Final-Project/images/server/images/Screen%20Shot%202020-04-06%20at%208.02.30%20PM.png"></Image>
                <br/>
                <br/>
            </div>
        )
    }
}

export default IntroPosts