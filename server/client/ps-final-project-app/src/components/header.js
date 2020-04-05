import React from 'react';
import { Component} from 'react'
import { Link } from "react-router-dom"
import './header.css'
import Modal from 'react-bootstrap/Modal'
import DictionaryEntry from "./dictionaryEntry.js"

class Header extends Component{
    constructor () {
        super()

        this.state = {
            show: false
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
                <div className="header">
                    <Link to={"/user"}><span className="user-icon"><i class="fas fa-user fa-1x"></i></span></Link>
                    <Link to={"/posts"}><span className="header-text">Cloze Weibo</span></Link>
                    <span className="search-icon"><i class="fas fa-search fa-1x" onClick={() => {this.setState({show:true})}}></i></span>
                </div>
            </div>
        )
    }
}

export default Header;