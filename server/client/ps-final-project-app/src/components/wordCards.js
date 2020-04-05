import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Image, Row, Col, ModalBody } from 'react-bootstrap'
import './wordCards.css'

class WordCards extends Component{

    renderWord(word) {
        return (
            <Row>
                <Col s={10}>
                    <div className="word-card">
                        <Row>
                            <Col s={12}>
                                <div className="simplified-traditional">
                                    <span className="simplified-char">{word.simplified}</span>
                                    <span className="traditional-char">({word.traditional})</span>
                                </div>
                            </Col>
                        </Row>
                        <Row>
                            <Col s={12}>
                                <div className="pinyin">
                                    {word.pinyin}
                                </div>
                                <div className="entry-POS">{word.partOfSpeech}</div>
                            </Col>
                        </Row>
                        <Row>
                            <Col s={12}>
                                <div className="english-definition">
                                    {word.english}
                                </div>
                            </Col>
                        </Row>
                    </div>
                </Col>
            </Row>
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

    