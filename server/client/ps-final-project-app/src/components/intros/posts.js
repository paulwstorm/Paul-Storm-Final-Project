import React from 'react';
import { Component } from 'react'
import { Button, Card, Row, Col } from 'react-bootstrap'
import './intro.css'



class IntroPosts extends Component {
    render() {
        return (
            <div>
                <h3 className="intro-header">Welcome to Posts!</h3>
                <p className="intro-paragraph">On this page you can see read of the recent posts tailored to your reading level!</p>
                <p className="intro-paragraph">These posts come from various Chinese social media and news outlets</p>
            </div>
        )
    }
}

export default IntroPosts