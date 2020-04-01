import React from 'react';
import { Component } from 'react'
import { Row, Col } from 'react-bootstrap'
import './header.css'

class Header extends Component{
    render() {
        return (
            <div className="header">
                <div className="headerText">Cloze Weibo</div>
            </div>
        )
    }
}

export default Header;