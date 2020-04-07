import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Row, Col } from 'react-bootstrap'
import './postClozes.css'
import Header from "./header.js"
import PostClozeCards from "./postClozeCards.js"
import * as actions from "../actions/index.js"
import Modal from 'react-bootstrap/Modal'
import IntroClozes from "./intros/clozes.js"

class PostClozes extends Component{
    constructor() {
        super()

        this.state = {
            showIntroModal: false
        }
    }

    async componentDidMount() {
        this.props.getPostClozes(this.props.viewNum, this.props.startPost)
        await this.props.getUser()
    }

    async checkNewUser() {
        if (Object.keys(this.props.user).length > 0) {
            if ((!this.props.user.visited.includes("/posts/clozes")) && (this.state.showIntroModal == false)) {
                this.setState({showIntroModal: true})
                await this.props.addRoomToUser("/posts/clozes")
            }
        }

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
                            <Button className="posts-clozes-more-posts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        } else if (this.props.startPost > 90) {
            return (
                <Row>
                <Col xs={2}></Col>
                    <Col xs={8}>
                        <Button className="lposts-clozes-less-posts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.prps.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                    </Col>
                <Col xs={2}></Col>
            </Row>  
            )
        }
    }

    render() {
        this.checkNewUser()
        if (this.props.clozes.length == 0) {
            return (
                <div>
                    <Header />
                    <Row>
                        <Col xs={4}></Col>
                        <Col xs={4}>
                            <h2 className="loading">Loading Clozes!</h2>
                        </Col>
                        <Col xs={4}></Col>
                    </Row>
                </div>
            )} else {
                return (
                    <div>
                        <Header />
                        <Modal
                        className="intro-modal"
                        size={"s"} 
                        show={this.state.showIntroModal} 
                        onHide={() => {this.setState({showIntroModal:false})}}>
                            <Modal.Body class="dictionary-body">
                                <IntroClozes></IntroClozes>
                            </Modal.Body>
                        </Modal>
                        <Row>
                            <Col xs={2}></Col>
                                <Col xs={8}>
                                    <Button className="posts-clozes-read-posts" href="/posts/">Read</Button>
                                    <Button className="posts-clozes-cloze-posts" href="/posts/clozes">Challenge</Button>
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
        startPost: state.startPost,
        user: state.user
    }
}

export default connect(mapStateToProps, actions)(PostClozes)