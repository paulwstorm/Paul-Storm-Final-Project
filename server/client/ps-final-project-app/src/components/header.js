import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Link } from "react-router-dom"
import './header.css'
import * as actions from "../actions/index.js"
import Modal from 'react-bootstrap/Modal'
import DictionaryEntry from "./dictionaryEntry.js"

class Header extends Component{
    constructor () {
        super()

        this.state = {
            show: false
        }
    }

    async componentDidMount() {
        // await this.props.getUser()
    }

    userNotSignedIn() {
        alert("Click a level to begin!")
    }

    renderUserIcon() {
        if (Object.keys(this.props.user).length > 0) {
            return (
                <Link to={"/user"}><span className="user-icon"><i class="fas fa-user fa-1x"></i></span></Link>
            )
        } else {
            return (
                <span className="user-icon" onClick={event => {this.userNotSignedIn()}}><i class="fas fa-user fa-1x"></i></span>
            )
        }
    }

    renderSearchIcon() {
        if (Object.keys(this.props.user).length > 0) {
            return (
                <span className="search-icon"><i class="fas fa-search fa-1x" onClick={() => {this.setState({show:true})}}></i></span>
            )
        } else {
            return (
                <span className="search-icon" onClick={event => {this.userNotSignedIn()}}><i class="fas fa-search fa-1x"></i></span>
            )
        }
    }

    render() {
        this.props.getUser()
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
                <div className="header">
                    <Link to={"/user"}><span className="user-icon"><i class="fas fa-user fa-1x"></i></span></Link>
                    <Link to={"/posts"}><span className="header-text">Cloze Weibo</span></Link>
                    <span className="search-icon" onClick={event => {this.userNotSignedIn()}}><i class="fas fa-search fa-1x"></i></span>
                </div>
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        user: state.user
    }
}

export default connect(mapStateToProps, actions)(Header)