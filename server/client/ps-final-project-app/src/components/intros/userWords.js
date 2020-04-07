import React from 'react';
import { Component } from 'react'
import { Button, Card, Row, Col, Image } from 'react-bootstrap'
import './intro.css'

class IntroUserWords extends Component {
    render() {
        return (
            <div>
                <h3 className="intro-header">Welcome to You Dictionary!</h3>
                <p className="intro-paragraph">
                    If you don't see any words here go back
                    to the posts page and click on any word in the post.
                    Once the defintion pops up click the plus symbol.
                </p>
                <br/>
                <p className="intro-paragraph">
                    Here you can see all the words you saved into your dictionary.
                    Use these buttons to toggle between reading the word defintions
                    and challening your vocabulary retention!
                </p>
            </div>
        )
    }
}

export default IntroUserWords