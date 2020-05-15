import React from 'react';
import { Component } from 'react'
import { Button, Card, Row, Col, Image } from 'react-bootstrap'
import './intro.css'

class IntroUserClozes extends Component {
    render() {
        return (
            <div>
                <h3 className="intro-header">These are your saved posts!</h3>
                <p className="intro-paragraph">
                    Here you can see all of the posts that you have saved.
                    As well as all of the posts have you filled-in-the-blank with.
                    By default you will only see the posts you recently saved and 
                    those posts you answered incorrectly last time. Select "All" to
                    see all of the posts you saved.
                </p>
            </div>
        )
    }
}

export default IntroUserClozes