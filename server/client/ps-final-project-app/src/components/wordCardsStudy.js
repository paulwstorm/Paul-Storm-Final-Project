import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Card, Row, Col } from 'react-bootstrap'
import Modal from 'react-bootstrap/Modal'
import './wordCardsStudy.css'

class WordCards extends Component{
    constructor () {
        super()

        this.state = {
            wordBack: {},
            show: false
        }
    }

    renderWord(word) {
        return (
            <Row>
                <Col s={10}>
                    <div>
                        <Row>
                            <Col md={2}></Col>
                            <Col md={8}>
                                <Card className="word-study-card" onClick={event => {this.setState({ wordBack: word}); this.setState({show: true})}}>
                                    <div class="card-body">
                                        {word.simplified}
                                    </div>
                                </Card>
                            </Col>
                            <Col md={2}></Col>
                        </Row>
                    </div>
                </Col>
            </Row>    
        )
    }

    render() {
        return (
            <div>
                <Modal
                className="word-modal"
                id="word-modal"
                size={"s"} 
                show={this.state.show} 
                onHide={() => {this.setState({show:false})}}>
                    <Modal.Body class="word-body">
                        <div>
                            <Row>
                                <Col s={12}>
                                    <div className="simplified-traditional">
                                        <span className="simplified-char">{this.state.wordBack.simplified}</span>
                                        <span className="traditional-char">({this.state.wordBack.traditional})</span>
                                    </div>
                                </Col>
                            </Row>
                            <Row>
                                <Col s={12}>
                                    <div className="pinyin">
                                        {this.state.wordBack.pinyin}
                                    </div>
                                    <div className="entry-POS">{this.state.wordBack.partOfSpeech}</div>
                                </Col>
                            </Row>
                            <Row>
                                <Col s={12}>
                                    <div className="english-definition">
                                        {this.state.wordBack.english}
                                    </div>
                                </Col>
                            </Row>
                        </div>
                    </Modal.Body>
                </Modal>
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

    