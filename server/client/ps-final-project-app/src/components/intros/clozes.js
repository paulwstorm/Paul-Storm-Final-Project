import React from 'react';
import { Component } from 'react'
import { Button, Card, Row, Col, Image } from 'react-bootstrap'
import './intro.css'

class IntroClozes extends Component {
    render() {
        return (
            <div>
                <h3 className="intro-header">Welcome to the Challenge!</h3>
                <p className="intro-paragraph">
                    Here you can see the same posts you were just reading
                    but here you are challenged to fill-in-the-blank with
                    the word that has been removed from the post
                </p>
                <p className="intro-paragraph">The [------] represents the space the word has been taken from</p>
                <br/>
                <p className="intro-paragraph">
                    Click on of the four boxes at the bottom to fill in the blank!
                </p>
            </div>
        )
    }
}

export default IntroClozes