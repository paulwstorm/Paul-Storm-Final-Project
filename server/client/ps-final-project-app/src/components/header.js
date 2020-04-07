import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Link } from "react-router-dom"
import './header.css'
import * as actions from "../actions/index.js"

class Header extends Component{
    constructor () {
        super()

        this.state = {
            show: false
        }
    }

    async componentDidMount() {
        await this.props.getUser()
    }

    renderUserIcon() {
        if (Object.keys(this.props.user).length > 0) {
            return (
                <Link to={"/user"}><span className="user-icon"><i class="fas fa-user fa-1x"></i></span></Link>
            )
        }
    }

    renderSearchIcon() {
        console.log(this.props.user)
        if (Object.keys(this.props.user).length > 0) {
            return (
                <span className="search-icon"><i class="fas fa-search fa-1x" onClick={() => {this.setState({show:true})}}></i></span>
            )
        }
    }

    render() {
        this.props.getUser()
        return (
            <div>
                <div className="header">
                    {this.renderUserIcon()}
                    <Link to={"/posts"}><span className="header-text">Cloze Weibo</span></Link>
                    {this.renderSearchIcon()}
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