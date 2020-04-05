import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Row, Col } from 'react-bootstrap'
import './userClozes.css'
import Header from "./header.js"
import PostClozeCards from "./postClozeCards.js"
import * as actions from "../actions/index.js"

class UserClozes extends Component{
    constructor () {
        super()

        this.state = {
            show: false,
            view: "incorrect",
            incorrectButton: "button-on",
            allButton: "button-off"
        }
    }

    componentDidMount() {
        this.props.getUserClozes(this.props.viewNum, this.props.startPost, this.state.view)
    }

    async handleToggleClick(view) {
        await this.setState({view: view})
        this.props.getUserClozes(this.props.viewNum, this.props.startPost, this.state.view)
    }

    renderButtons() {
        if (this.props.startPost > 9 && this.props.startPost <= 90 ) {
            return (
                <Row>
                    <Col xs={1}></Col>
                        <Col xs={10}>
                            <Button className="posts-clozes-less-posts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                            <Button className="posts-clozes-more-posts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>
                        </Col>
                    <Col xs={1}></Col>
                </Row>  
            )
        } else if (this.props.startPost < 10) {
            return (
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className="posts-clozes-more-posts" onClick={event => { this.props.getUserClozes(this.props.viewNum, (this.props.startPost + 10), this.state.view); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        } else if (this.props.startPost > 90) {
            return (
                <Row>
                <Col xs={2}></Col>
                    <Col xs={8}>
                        <Button className="lposts-clozes-less-posts" onClick={event => { this.props.getUserClozes(this.props.viewNum, (this.props.startPost - 10), this.state.view); this.props.decrementPostNumber(this.prps.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                    </Col>
                <Col xs={2}></Col>
            </Row>  
            )
        }
    }

    render() {
        if (this.props.clozes.length == 0) {
            return (
                <div>
                    <Header />
                    <Row>
                        <Col xs={4}></Col>
                        <Col xs={4}>
                            <h2 className="loading">See your saved posts here!</h2>
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
                                    <Button className={this.state.incorrectButton} onClick={() => {this.handleToggleClick("incorrect"); this.setState({allButton: "button-off"}); this.setState({incorrectButton: "button-on"})}}>Incorrect</Button>
                                    <Button className={this.state.allButton} onClick={() => {this.handleToggleClick("all"); this.setState({incorrectButton: "button-off"}); this.setState({allButton: "button-on"})}}>All</Button>
                                </Col>
                            <Col xs={2}></Col>
                        </Row>  
                        <PostClozeCards />
                        { this.renderButtons() }
                    </div>
                )
            }
        }
}

function mapStateToProps(state) {
    return {
        clozes: state.clozes,
        viewNum: state.viewNum,
        startPost: state.startPost
    }
}

export default connect(mapStateToProps, actions)(UserClozes)