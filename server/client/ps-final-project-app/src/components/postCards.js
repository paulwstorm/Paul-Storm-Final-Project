import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Image, Row, Col } from 'react-bootstrap'
import './postCards.css'
import * as actions from "../actions/index.js"

class PostCards extends Component{
    renderPosts(post) {
        console.log(post)
        if (post.postSource == "weibo") {
            return (
                <div>
                    <Row>
                        <Col sm={2}></Col>
                        <Col sm={8}>
                            <Card className="postCard" shadow>
                                <div class="card-body">
                                    <div className="user"><Image className="userImage" roundedCircle fluid src={post.postUserImageUrl} /><span>{post.postUser}</span><i class="fab fa-weibo fa-2x"></i></div>
                                    <div className="postContent">{ post.postContent }</div>
                                    <div className="cardBotom"><span className="postPopularity">{post.postPopularity}</span><Button className="userUrl" href={`https://www.weibo.com/${post.postUserUrl}`} target='_blank'>See User</Button></div>
                                </div>
                            </Card>
                        </Col>
                        <Col sm={2}></Col>
                    </Row>
                </div>
            )
        } else if (post.postSource == "zhihu_recommended" || post.postSource == "zhihu_hot") {
            return (
                <div>
                    <Row>
                        <Col sm={2}></Col>
                        <Col sm={8}>
                            <Card className="postCard">
                                <i class="fab fa-zhihu fa-2x"></i>
                                <div>{ post.postContent }</div>
                            </Card>
                        </Col>
                        <Col sm={2}></Col>
                    </Row>
                </div>
            )
        }
    }
    render() {
        return (
            this.props.posts.map(post => (this.renderPosts(post)))
        )
    }
}

function mapStateToProps(state) {
    return {
        posts: state.posts
    }
}

export default connect(mapStateToProps, actions)(PostCards)

    