import React from 'react';
import { Component } from 'react'
import { Button, Card, Row, Col, Image } from 'react-bootstrap'
import './intro.css'



class IntroPosts extends Component {
    render() {
        return (
            <div>
                <h3 className="intro-header">Welcome to Posts!</h3>
                <p className="intro-paragraph">On this page you can see read of the recent posts tailored to your reading level!</p>
                <p className="intro-paragraph">This is an example post:</p>
                <Image className="sample-post" src="https://raw.githubusercontent.com/paulwstorm/Paul-Storm-Final-Project/master/server/images/Screen%20Shot%202020-04-06%20at%207.29.37%20PM.png"></Image>
                <p className="intro-paragraph">
                    For this post, the user is on the top left.
                    Whatever the post, clicking on the top left hand corner with talk you the post source.
                </p>
            </div>
        )
    }
}

export default IntroPosts