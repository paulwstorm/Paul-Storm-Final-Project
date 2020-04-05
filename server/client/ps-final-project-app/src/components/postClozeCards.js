import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Image, Row, Col } from 'react-bootstrap'
import './postClozeCards.css'
import * as actions from "../actions/index.js"
import Modal from 'react-bootstrap/Modal'
import DictionaryEntry from "./dictionaryEntry.js"

class PostClozeCards extends Component{
    constructor () {
        super()

        this.state = {
            show: false,
            searchTerm: ""
        }

        this.wordOnClick = this.wordOnClick.bind(this)
    }

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

    renderPostWords(postContent) {
        return (
            postContent.map(word => {
                return <span onClick={() => {this.setState({show: true}); this.wordOnClick(word[0])}}>{ word[0] }</span>
            })
        )
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
                    <Col sm={10}><div>{ this.renderPostWords(post.postClozedTokenizedContent) }</div></Col>
                    <Col sm={1}></Col>
                </Row>
            )
        } else {
            return (
                <Row className="zhihuContent">
                    <Col xs={8}><div>{ this.renderPostWords(post.postClozedTokenizedContent) }</div></Col>
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
                                    <Row>
                                        <Col xs={7}>
                                            <a href={`https://www.weibo.com/${post.postUserUrl}`} target='_blank'>
                                                <Image className="userImage" roundedCircle fluid src={post.postUserImageUrl} />
                                                <span>{post.postUser}</span>
                                            </a>
                                        </Col>
                                        <Col xs={5}><div><i class="fab fa-zhihu fa-2x"></i></div></Col>
                                    </Row>                                    <div className="postContent">{ this.renderPostWords(post.postClozedTokenizedContent) }</div>
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[0] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[0] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[1] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[1] }</Button>
                                        </Col>   
                                        <Col xs={2}></Col>     
                                    </Row>
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[2] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[2] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[3] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[3] }</Button>
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
                                        <Col xs={7}>
                                            <a className="postUrl" href={post.postUrl} target='_blank'> 
                                                Zhihu Question:
                                            </a>   
                                        </Col>
                                        <Col xs={5}><div><i class="fab fa-zhihu fa-2x"></i></div></Col>
                                    </Row>
                                    { this.renderContentImage(post)}
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[0] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[0] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[1] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[1] }</Button>
                                        </Col>   
                                        <Col xs={2}></Col>     
                                    </Row>
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[2] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[2] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[3] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[3] }</Button>
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
                                        <Col xs={5}><div><i class="far fa-newspaper fa-2x"></i></div></Col>
                                    </Row>
                                    { this.renderContentImage(post)}
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[0] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[0] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[1] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[1] }</Button>
                                        </Col>   
                                        <Col xs={2}></Col>     
                                    </Row>
                                    <Row className="multipleChoiceTop">     
                                        <Col xs={2}></Col>
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[2] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[2] }</Button>
                                        </Col>                               
                                        <Col xs={4}>
                                            <Button className="multiple-choice" value={ post.multipleChoiceWords[3] } onClick={event => {this.checkCorrect(event.target.value, post.removedWord, post)}}>{ post.multipleChoiceWords[3] }</Button>
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
                {this.props.clozes.map(post => (this.renderPosts(post)))}
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        clozes: state.clozes,
        searchTerm: state.searchTerm
    }
}

export default connect(mapStateToProps, actions)(PostClozeCards)

    