import React from 'react';
import { Component, Link } from 'react'
import { connect } from "react-redux"
import { Button, Card, Row, Col } from 'react-bootstrap'
import './userWords.css'
import Header from "./header.js"
import WordCards from "./wordCards.js"
import * as actions from "../actions/index.js"

class UserWords extends Component {
    componentDidMount() {
        this.props.getWords(this.props.viewNum, this.props.startPost)
    }

    renderButtons() {
        if (this.props.startPost > 9 && this.props.startPost <= 90 ) {
            return (
                <Row>
                    <Col xs={1}></Col>
                        <Col xs={10}>
                            <Button className="words-less-words" onClick={event => { this.props.getWords(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                            <Button className="words-more-words" onClick={event => { this.props.getWords(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>
                        </Col>
                    <Col xs={1}></Col>
                </Row>  
            )
        } else if (this.props.startPost < 10) {
            return (
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className="words-more-words" onClick={event => { this.props.getWords(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        } else if (this.props.startPost > 90) {
            return (
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className="words-less-words" onClick={event => { this.props.getWords(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.prps.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        }
    }

    render() {
        if (this.props.words.length == 0) {
            return (
                <div>
                    <Header />
                    <Row>
                        <Col xs={4}></Col>
                        <Col xs={4}>
                            <h2 className="loading">Loading Words!</h2>
                        </Col>
                        <Col xs={4}></Col>
                    </Row>
                </div>
            )} else {
                return (
                    <div>
                        <Header />
                        <Row>
                            <Col xs={2}></Col>
                                <Col xs={8}>
                                    <Button className="words-read-words" href="/user/words">Read</Button>
                                    <Button className="words-study-words" href="/user/words/study">Study</Button>
                                </Col>
                            <Col xs={2}></Col>
                        </Row>  
                        <WordCards />
                        { this.renderButtons() }
                    </div>
                )
            }
        }
}

function mapStateToProps(state) {
    return {
        words: state.words,
        viewNum: state.viewNum,
        startPost: state.startPost
    }
}

export default connect(mapStateToProps, actions)(UserWords)