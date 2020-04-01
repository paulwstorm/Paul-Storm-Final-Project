import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Card, Row, Col } from 'react-bootstrap'
import './posts.css'
import Header from "./header.js"
import * as actions from "../actions/index.js"

class Posts extends Component{
    constructor() {
        super()

        this.state = {
            viewNum: 10
        }
    }

    componentDidMount() {
        this.props.getPosts(this.state.viewNum)
    }

    renderPost() {
        return (
            <div>
                <Header />
                <Row>
                    <Col sm={3}></Col>
                    <Col sm={6}>
                        <Card>
                            <div>Posts will go where!</div>
                        </Card>
                    </Col>
                    <Col sm={3}></Col>
                </Row>
            </div>
        )
    }
    render() {
        if (this.props.posts == undefined) {
            return (
                <div>
                    <Header />
                    <Row>
                        <Col sm={3}></Col>
                        <Col sm={6}>
                            <Card>
                                <div>Loading!</div>
                            </Card>
                        </Col>
                        <Col sm={3}></Col>
                    </Row>
                </div>
            )} else {
                return (
                    this.renderPosts()
                )
            }
        }
}

function mapStateToProps(state) {
    return {
        posts: state.posts
    }
}

export default connect(mapStateToProps, actions)(Posts)