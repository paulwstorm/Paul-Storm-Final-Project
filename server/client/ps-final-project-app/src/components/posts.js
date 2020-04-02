import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Row, Col } from 'react-bootstrap'
import './posts.css'
import Header from "./header.js"
import PostCards from "./postCards.js"
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

    render() {
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
                        <PostCards />    
                    </div>
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