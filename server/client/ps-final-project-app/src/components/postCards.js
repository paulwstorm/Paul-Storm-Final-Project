import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Image, Row, Col, ModalBody } from 'react-bootstrap'
import { Link } from "react-router-dom"
import Modal from 'react-bootstrap/Modal'
import './postCards.css'
import DictionaryEntry from "./dictionaryEntry.js"
import * as actions from "../actions/index.js"

class PostCards extends Component{
    constructor () {
        super()

        this.state = {
            show: false
        }
    }

    renderPostWords(postContent) {
        return (
            postContent.map(word => {
                return <span onClick={() => {this.setState({show: true}); this.wordOnClick(word[0])}}>{ word[0] }</span>
            })
        )
    }

    addClozeButton(post) {
        this.props.addClozeToUser(post)
        alert("Post added for study!")
    }

    async wordOnClick(word) {
        await this.props.newSearchTerm(word)
        this.props.wordSearch(this.props.searchTerm)
    }

    renderContentImage(post) {
        if (post.postImageUrl.length == 0) {
            return (
                <Row className="zhihuContent">
                    <Col sm={1}></Col>
                    <Col sm={10}><div className="postContent">{ this.renderPostWords(post.postTokenizedContent) }</div></Col>
                    <Col sm={1}></Col>
                </Row>
            )
        } else {
            return (
                <Row className="zhihuContent">
                    <Col xs={8}><div className="postContent">{ this.renderPostWords(post.postTokenizedContent) }</div></Col>
                    <Col xs={4}><img className="zhihuImage" src={post.postImageUrl} onError={(e)=>{e.target.onerror = null; e.target.src="http://pic.51yuansu.com/pic/cover/00/05/24/5736985738490_610.jpg"}} /></Col>
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
                        <Col md={2}></Col>
                        <Col md={8}>
                            <Card className="postCard">
                                <div class="card-body">
                                    <Row>
                                        <Col md={7}>
                                            <div className="user">
                                                <a href={`https://www.weibo.com/${post.postUserUrl}`} target='_blank'>
                                                        <Image className="userImage" roundedCircle fluid src={post.postUserImageUrl} />
                                                        <span>{post.postUser}</span>
                                                </a>
                                            </div>
                                        </Col>
                                        <Col md={2}><div className="postLevel">Level: {post.postLevel}</div></Col>
                                        <Col md={3}>
                                            <div className="source-icon">
                                                <span className="source">source:</span>
                                                <i class="fab fa-weibo fa-2x"></i>
                                            </div>
                                        </Col>
                                    </Row>
                                    <div className="postContent">{ this.renderPostWords(post.postTokenizedContent) }</div>
                                    <Row className="cardBotom">     
                                            <Col xs={6}><div className="postDate">{post.dateRetrieved.slice(0,10)}</div></Col>
                                            <Col xs={6}><span class="material-icons addCloze" onClick={() => {this.addClozeButton(post)}}>add_circle_outline</span></Col>
                                    </Row>
                                </div>
                            </Card>
                        </Col>
                        <Col md={2}></Col>
                    </Row>
                </div>
            )
        } else if (post.postSource == "zhihu_recommended" || post.postSource == "zhihu_hot") {
            return (
                <div>
                    <Row>
                        <Col md={2}></Col>
                        <Col md={8}>
                            <Card className="postCard">
                                <div class="card-body">
                                    <Row>
                                        <Col xs={5}>
                                            <a className="postUrl" href={post.postUrl} target='_blank'> 
                                                Zhihu Question:
                                            </a>   
                                        </Col>
                                        <Col xs={7}>
                                            <div>
                                                <span className="postLevel">Level: {post.postLevel}</span>
                                                <span className="source-icon">
                                                    <span className="source">source:</span>
                                                    <i class="fab fa-zhihu fa-2x"></i>
                                                </span>
                                            </div>
                                        </Col>
                                    </Row>
                                    { this.renderContentImage(post)}
                                    <Row className="cardBotom">                                    
                                        <Col xs={6}><div className="postDate">{post.dateRetrieved.slice(0,10)}</div></Col>
                                        <Col xs={6}><span class="material-icons addCloze" onClick={() => {this.addClozeButton(post)}}>add_circle_outline</span></Col>
                                    </Row>
                                </div>
                            </Card>
                        </Col>
                        <Col md={2}></Col>
                    </Row>
                </div>
            )
        } else if (post.postSource.slice(0,6) == "wangyi" || post.postSource.slice(0,7) == "toutiao") {
            return (
                <div>
                    <Row>
                        <Col md={2}></Col>
                        <Col md={8}>
                            <Card className="postCard">
                                <div class="card-body">
                                    <Row>
                                        <Col xs={7}>
                                            <a className="postUrl" href={post.postUrl} target='_blank'>News Article:</a>
                                        </Col>
                                        <Col xs={5}>
                                            <div>
                                                <span className="postLevel">Level: {post.postLevel}</span>
                                                <span className="source-icon">
                                                    <span className="source">source:</span>
                                                    <i class="far fa-newspaper fa-2x"></i>
                                                </span>
                                            </div>
                                        </Col>
                                    </Row>
                                        <div className="postContent">
                                            { this.renderContentImage(post)}
                                        </div>
                                    <Row className="cardBotom">                                    
                                        <Col xs={6}><div className="postDate">{post.dateRetrieved.slice(0,10)}</div></Col>
                                        <Col xs={6}><span class="material-icons addCloze" onClick={() => {this.addClozeButton(post)}}>add_circle_outline</span></Col>
                                    </Row>
                                </div>
                            </Card>
                        </Col>
                        <Col md={2}></Col>
                    </Row>
                </div>
            )
        }
    }

    render() {
        return (
            <div>
                <Modal
                className="dictionary-modal"
                id="dict-modal"
                size={"s"} 
                show={this.state.show} 
                onHide={() => {this.setState({show:false})}}>
                    <Modal.Body class="dictionary-body">
                        <DictionaryEntry></DictionaryEntry>
                    </Modal.Body>
                </Modal>
                {this.props.posts.map(post => (this.renderPosts(post)))}
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        posts: state.posts,
        searchTerm: state.searchTerm
    }
}

export default connect(mapStateToProps, actions)(PostCards)

    