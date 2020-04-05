import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Image, Row, Col, ModalBody } from 'react-bootstrap'
import './wordCards.css'

class WordCards extends Component{

    renderWord(word) {
        return (
            <div>
                <Row>
                    <Col md={2}></Col>
                    <Col md={8}>
                        <Card className="postCard">
                            <div class="card-body">
                                {word.simplified}
                            </div>
                        </Card>
                    </Col>
                    <Col md={2}></Col>
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

    