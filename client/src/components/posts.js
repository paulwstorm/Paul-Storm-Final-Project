import React from 'react';
import { Component, Link } from 'react'
import { connect } from "react-redux"
import { Button, Card, Row, Col } from 'react-bootstrap'
import './posts.css'
import Header from "./header.js"
import PostCards from "./postCards.js"
import * as actions from "../actions/index.js"
import Modal from 'react-bootstrap/Modal'
import IntroPosts from "./intros/posts.js"


class Posts extends Component{
    constructor() {
        super()

        this.state = {
            viewNum: 10,
            startPost: 0,
            showIntroModal: false
        }

        this.initialPosts = this.initialPosts.bind(this)
    }

    async componentDidMount() {
        this.initialPosts()
        await this.props.getUser()
    }

    initialPosts() {
        if (this.props.posts.length === 0) {
            console.log("no posts yet")
            this.props.getPosts(this.props.viewNum, this.props.startPost)
            setTimeout(() => {this.initialPosts()}, 10000)
        } else {
            console.log("posts")
        }
    }

    async checkNewUser() {
        if (Object.keys(this.props.user).length > 0) {
            if ((!this.props.user.visited.includes("/posts")) && (this.state.showIntroModal == false)) {
                this.setState({showIntroModal: true})
                await this.props.addRoomToUser("/posts")
            }
        }
    }

    renderButtons() {
        if (this.props.startPost > 9 && this.props.startPost <= 90 ) {
            return (
                <Row>
                    <Col xs={1}></Col>
                        <Col xs={10}>
                            <Button className="posts-less-posts" onClick={event => { this.props.getPosts(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                            <Button className="posts-more-posts" onClick={event => { this.props.getPosts(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>
                        </Col>
                    <Col xs={1}></Col>
                </Row>  
            )
        } else if (this.props.startPost < 10) {
            return (
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className="posts-more-posts" onClick={event => { this.props.getPosts(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        } else if (this.props.startPost > 90) {
            return (
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className="posts-less-posts" onClick={event => { this.props.getPosts(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.prps.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        }
    }

    render() {
        this.checkNewUser()
        if (this.props.posts.length == 0) {
            return (
                <div>
                    <Header />
                    <Row>
                        <Col xs={4}></Col>
                        <Col xs={4}>
                            <h2 className="loading">Loading Posts!</h2>
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
                            <Modal.Body class="intro-body">
                                <IntroPosts></IntroPosts>
                            </Modal.Body>
                        </Modal>
                        <Row>
                            <Col xs={2}></Col>
                                <Col xs={8}>
                                    <Button className="posts-read-posts" href="/posts/">Read</Button>
                                    <Button className="posts-cloze-posts" href="/posts/clozes">Challenge</Button>
                                </Col>
                            <Col xs={2}></Col>
                        </Row>  
                        <PostCards />
                        { this.renderButtons() }
                    </div>
                )
            }
        }
}

function mapStateToProps(state) {
    return {
        posts: state.posts,
        viewNum: state.viewNum,
        startPost: state.startPost,
        user: state.user
    }
}

export default connect(mapStateToProps, actions)(Posts)