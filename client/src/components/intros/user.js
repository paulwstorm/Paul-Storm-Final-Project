import React from 'react';
import { Component } from 'react'
import { Button, Card, Row, Col, Image } from 'react-bootstrap'
import './intro.css'

class IntroClozes extends Component {
    render() {
        return (
            <div>
                <h3 className="intro-header">Welcome to You User Page!</h3>
                <p className="intro-paragraph">
                    Here you can see all the words you saved from the dictionary
                    as well as all of the post you have saved or attempted to fill in the blank.
                </p>
            </div>
        )
    }
}

export default IntroClozes