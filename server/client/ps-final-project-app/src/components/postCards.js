import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Image, Row, Col } from 'react-bootstrap'
import './postCards.css'
import * as actions from "../actions/index.js"

class PostCards extends Component{
    renderZhihuContent(post) {
        if (post.postImageUrl.length == 0) {
            return (
                <Row className="zhihuContent">
                    <Col sm={1}></Col>
                    <Col sm={10}><div>{ post.postContent }</div></Col>
                    <Col sm={1}></Col>
                </Row>
            )
        } else {
            return (
                <Row className="zhihuContent">
                    <Col xs={8}><div>{ post.postContent }</div></Col>
                    <Col xs={4}><Image className="zhihuImage" src={post.postImageUrl}/></Col>
                </Row>
            )
        }
    }

    renderPosts(post) {
        console.log(post)
        if (post.postSource == "weibo") {
            return (
                <div>
                    <Row>
                        <Col sm={2}></Col>
                        <Col sm={8}>
                            <Card className="postCard">
                                <div class="card-body">
                                    <div className="user"><Image className="userImage" roundedCircle fluid src={post.postUserImageUrl} /><span>{post.postUser}</span><i class="fab fa-weibo fa-2x"></i></div>
                                    <div className="postContent">{ post.postContent }</div>
                                    <Row className="cardBotom">                                    
                                            <Col xs={4}><div className="postPopularity">{post.postPopularity}</div></Col>
                                            <Col xs={4}><Button className="userUrl" href={`https://www.weibo.com/${post.postUserUrl}`} target='_blank'>See User</Button></Col>
                                            <Col xs={4}><span class="material-icons addCloze">add_circle_outline</span></Col>
                                    </Row>
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
                                <div class="card-body">
                                    <Row>
                                        <Col xs={7}></Col>
                                        <Col xs={5}><div><i class="fab fa-zhihu fa-2x"></i></div></Col>
                                    </Row>
                                    { this.renderZhihuContent(post)}
                                    <Row className="cardBotom">                                    
                                        <Col xs={4}><div className="postPopularity">{post.postPopularity}</div></Col>
                                        <Col xs={4}><Button className="userUrl" href={`https://www.weibo.com/${post.postUrl}`} target='_blank'>See on Zhihu</Button></Col>
                                        <Col xs={4}><span class="material-icons addCloze">add_circle_outline</span></Col>
                                    </Row>
                                </div>
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

    