import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Row, Col } from 'react-bootstrap'
import './postClozes.css'
import Header from "./header.js"
import PostClozeCards from "./postClozeCards.js"
import * as actions from "../actions/index.js"

class PostClozes extends Component{
    componentDidMount() {
        this.props.getPostClozes(this.props.viewNum, this.props.startPost)
    }

    renderButtons() {
        console.log(this.props.viewNum)
        console.log(this.props.startPost)
        if (this.props.startPost > 9 && this.props.startPost <= 90 ) {
            return (
                <Row>
                    <Col xs={1}></Col>
                        <Col xs={10}>
                            <Button className="lessPosts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                            <Button className="readPosts" href="/posts">Read</Button>
                            <Button className="morePosts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>
                        </Col>
                    <Col xs={1}></Col>
                </Row>  
            )
        } else if (this.props.startPost < 10) {
            return (
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className="readPosts" href="/posts">Read</Button>
                            <Button className="morePosts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        } else if (this.props.startPost > 90) {
            return (
                <Row>
                <Col xs={2}></Col>
                    <Col xs={8}>
                        <Button className="readPosts" href="/posts">Read</Button>
                        <Button className="lessPosts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.prps.viewNum); window.scrollTo(0, 0)}}>Back</Button>
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
                            <h2 className="loading">Loading Clozes!</h2>
                        </Col>
                        <Col xs={4}></Col>
                    </Row>
                </div>
            )} else {
                return (
                    <div>
                        <Header />
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

export default connect(mapStateToProps, actions)(PostClozes)