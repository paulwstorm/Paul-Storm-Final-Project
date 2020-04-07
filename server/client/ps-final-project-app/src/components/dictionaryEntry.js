import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Row, Col } from 'react-bootstrap'
import Modal from 'react-bootstrap/Modal'
import './dictionaryEntry.css'
import * as actions from "../actions/index.js"

class DictionaryEntry extends Component{

    componentDidMount() {
        this.props.wordSearch(this.props.searchTerm)
    }

    onEntryClick(word) {
        this.props.addWordToUserDict(word)
        alert(`${word.simplified} added to your dictionary!`)
    }

    async wordOnClick(word) {
        await this.props.newSearchTerm(word)
        this.props.wordSearch(this.props.searchTerm)
    }

    render() {
        if (this.props.word.length == 0 ) {
            return (
                <div>
                    <Row className="dictionary-top">
                        <h4 className="dictionary-title">Search the Dictionary:</h4>
                        <span>
                            <form className="input-group search-bar">
                                <input
                                    value={this.props.searchTerm}
                                    onChange={(event) => {console.log(event.target.value);this.wordOnClick(event.target.value)}}
                                />
                            </form>
                        </span>
                    </Row>
                    <div>searching the dictionary...</div>
                </div>
            )
        } else {
            return (
                <div>
                    <Row className="dictionary-top">
                        <h4 className="dictionary-title">Search the Dictionary:</h4>
                        <span>
                            <form className="input-group search-bar">
                                <input
                                    value={this.props.searchTerm}
                                    onChange={(event) => {console.log(event.target.value);this.wordOnClick(event.target.value)}}
                                />
                            </form>
                        </span>
                    </Row>
                    {
                    this.props.word.map((entry, index) => {
                        let entryNum = index + 1
                        return (
                            <div className="entry">
                                <Row>
                                    <Col s={12}>
                                        <div className="simplified-traditional">
                                            <span className= "entry-num">{entryNum}.</span>
                                            <span className="simplified-char">Character: {entry.simplified}</span>
                                            {/* <span className="traditional-char">({entry.traditional})</span> */}
                                            <span class="material-icons add-word" onClick={() => {this.onEntryClick(entry)}}>add_circle_outline</span>
                                        </div>
                                    </Col>
                                </Row>
                                <Row>
                                    <Col s={12}>
                                        <div className="pinyin">
                                        Pronunciation: {entry.pinyin}
                                        </div>
                                        <div className="entry-POS">
                                            Part of Speech: {entry.partOfSpeech}
                                        </div>
                                    </Col>
                                </Row>
                                <Row>
                                    <Col s={12}>
                                        <div className="english-definition">
                                            Definition: {entry.english}
                                        </div>
                                    </Col>
                                </Row>
                            </div>
                        )
                    })
                    }
                </div>
            )
        }
    }
}


function mapStateToProps(state) {
    return {
        word: state.searchResult,
        searchTerm: state.searchTerm
    }
}

export default connect(mapStateToProps, actions)(DictionaryEntry)