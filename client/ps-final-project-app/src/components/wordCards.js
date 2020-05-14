import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Image, Row, Col, ModalBody } from 'react-bootstrap'
import './wordCards.css'

class WordCards extends Component{

    renderWord(word) {
        return (
            <div className="word-card">
                <Row>
                    <Col s={12}>
                        <div className="simplified-traditional">
                            <span className="word-simplified-char">Character: {word.simplified}</span>
                            <span className="traditional-char">  ({word.traditional})</span>
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col s={12}>
                        <div className="word-pinyin">
                        Pronunciation: {word.pinyin}
                        </div>
                        <div className="word-POS">
                            Part of Speech: {word.partOfSpeech}
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col s={12}>
                        <div className="word-english-definition">
                            Definition: {word.english}
                        </div>
                    </Col>
                </Row>
            </div>
        )
    }

    render() {
        return (
            <div>
                {this.props.words.map(word => this.renderWord(word))}
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        words: state.words    
    }
}


export default connect(mapStateToProps)(WordCards)

    