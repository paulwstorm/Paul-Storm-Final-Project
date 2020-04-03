import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Image, Row, Col } from 'react-bootstrap'
import './postClozeCards.css'
import * as actions from "../actions/index.js"

class PostClozeCards extends Component{

    checkCorrect(guessed, answer, cloze) {
        if (guessed == answer) {
            alert("宝贝很棒哦！\n Correct!")
            let mark="correct"
            this.props.markClozeCorrect(mark, cloze, this.props.clozes)
        } else {
            alert("哎呀！宝贝要加油啊！\n Incorrect!")
            let mark="incorrect"
            this.props.markClozeCorrect(mark, cloze, this.props.clozes)
        }
    }
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
                    <Col xs={4}><img className="zhihuImage" src={post.postImageUrl} onError={(e)=>{e.target.onerror = null; e.target.src="http://pic.51yuansu.com/pic/cover/00/05/24/5736985738490_610.jpg"}} /></Col>
                </Row>
            )
        }
    }

    renderPosts(post) {
        if (post.postSource == "weibo") {
            return (
                <div>
                    <Row>
                        <Col md={2}></Col>
                        <Col md={8}>
                            <Card className="postCard">
                                <div class="card-body">
                                    <div className="user"><Image className="userImage" roundedCircle fluid src={post.postUserImageUrl} /><span>{post.postUser}</span><i class="fab fa-weibo fa-2x"></i></div>
                                    <div className="postContent">{ post.postContent }</div>
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multipleChoice" value={ post.multipleChoiceWords[0] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[0] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multipleChoice" value={ post.multipleChoiceWords[1] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[1] }</Button>
                                        </Col>   
                                        <Col xs={2}></Col>     
                                    </Row>
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multipleChoice" value={ post.multipleChoiceWords[2] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[2] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multipleChoice" value={ post.multipleChoiceWords[3] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[3] }</Button>
                                        </Col>   
                                        <Col xs={2}></Col>     
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
                                        <Col xs={7}></Col>
                                        <Col xs={5}><div><i class="fab fa-zhihu fa-2x"></i></div></Col>
                                    </Row>
                                    { this.renderZhihuContent(post)}
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multipleChoice" value={ post.multipleChoiceWords[0] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[0] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multipleChoice" value={ post.multipleChoiceWords[1] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[1] }</Button>
                                        </Col>   
                                        <Col xs={2}></Col>     
                                    </Row>
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multipleChoice" value={ post.multipleChoiceWords[2] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[2] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multipleChoice" value={ post.multipleChoiceWords[3] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[3] }</Button>
                                        </Col>   
                                        <Col xs={2}></Col>     
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
            this.props.clozes.map(post => (this.renderPosts(post)))
        )
    }
}

function mapStateToProps(state) {
    return {
        clozes: state.clozes
    }
}

export default connect(mapStateToProps, actions)(PostClozeCards)

    